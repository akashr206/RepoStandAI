import { createClient } from "@supabase/supabase-js";
import dotenv from "dotenv";
import { embed } from "../util/embed.js";
import { glob } from "glob";
import path from "path";
import fs from "fs";
dotenv.config();

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

export function splitChunks(content, size) {
    const chunks = [];

    const patterns = [
        // JS / TS functions
        `(?:async\\s+function\\s+\\w+\\s*\\([^)]*\\)\\s*\\{[\\s\\S]*?\\})`,
        `(?:function\\s+\\w+\\s*\\([^)]*\\)\\s*\\{[\\s\\S]*?\\})`,
        `(?:const\\s+\\w+\\s*=\\s*\\([^)]*\\)\\s*=>\\s*\\{[\\s\\S]*?\\})`,

        // Classes(JS, Java, C++)
        `(?:class\\s+\\w+\\s*\\{[\\s\\S]*?\\})`,

        // Python functions / classes
        `(?:def\\s+\\w+\\s*\\([^)]*\\):[\\s\\S]*?(?=\\n\\S|\\n$))`,
        `(?:class\\s+\\w+\\s*(?:\\([^)]*\\))?:[\\s\\S]*?(?=\\n\\S|\\n$))`,

        // Java / C / C++ methods
        `(?:(?:public|private|protected)?\\s*\\w[\\w<>\\[\\]]*\\s+\\w+\\s*\\([^)]*\\)\\s*\\{[\\s\\S]*?\\})`,

        // Go functions
        `(?:func\\s+\\w+\\s*\\([^)]*\\)\\s*\\{[\\s\\S]*?\\})`,

        // Rust functions
        `(?:fn\\s+\\w+\\s*\\([^)]*\\)\\s*\\{[\\s\\S]*?\\})`
    ];

    const regex = new RegExp(`(${patterns.join('|')})`, 'g');
    let match;

    while ((match = regex.exec(content)) !== null) {
        chunks.push(match[0]);
    }

    if (chunks.length === 0) {
        return chunkBySize(content, size);
    }

    return chunks;
}

function chunkBySize(text, size = 700) {
    const chunks = [];

    for (let i = 0; i < text.length; i += size) {
        chunks.push(text.slice(i, i + size));
    }

    return chunks;
}

function groupFiles(repoPath, files) {
    const groupedFiles = [];
    let tempContent = ""
    for (const file of files) {
        const filePath = path.join(repoPath, file);
        const content = file + ":- \n\n " + fs.readFileSync(filePath, "utf-8");
        if (content.length > 50030) {
            continue;
        }
        if (tempContent.length + content.length > 50000) {
            groupedFiles.push(tempContent);
            tempContent = "";
        }
        tempContent += content;
    }
    if (tempContent.length > 0) {
        groupedFiles.push(tempContent);
    }
    return groupedFiles;
}

const IGNORE_PATTERNS = [ 
    "**/node_modules/**",
    "**/.git",
    "**/.git/**",
    "**/.next/**",
    "**/dist/**",
    "**/build/**",
    "**/*.lock",
    "**/*.png",
    "**/*.jpg",
    "**/*.jpeg",
    "**/*.gif",
    "**/*.svg",
    "**/*.webp",
];

export async function embedFile(repoPath, repoId) {
    try {
        const files = await glob("**/*", {
            cwd: repoPath,
            nodir: true,
            ignore: IGNORE_PATTERNS,
        });

        console.log(`Embedding ${files.length} files`);
        const groupedFiles = groupFiles(repoPath, files); ``
        for (const content of groupedFiles) {
            console.log(`Embedding ${content.length} characters`);
            const chunks = splitChunks(content, 700);

            const { error, embeddings } = await embed(chunks);
            if (error) {
                console.log("error : ", error);
                return { error }
            }

            for (let i = 0; i < chunks.length; i++) {
                const { error: dbError } = await supabase.from("embeddings").insert({
                    repo_id: repoId,
                    embedding: embeddings[i],
                    content: chunks[i],
                })
                if (dbError) {
                    console.log("error : ", dbError);
                    return { error: dbError }
                }
            }
        }
        return { success: true }
    } catch (error) {
        console.log(error);
        return { error }
    }
}