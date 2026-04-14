import { createClient } from "@supabase/supabase-js";
import { glob } from "glob/raw";
import path from "path";
import fs from "fs";
import dotenv from "dotenv";

dotenv.config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);
const IGNORE_PATTERNS = [
    "**/node_modules/**",
    "**/.git/**",
    "**/.next/**",
    "**/dist/**",
    "**/build/**",
    "**/*.lock",
];
export async function storeRepo(LocalRepoPath, repoId) {
    try {
        const files = await glob("**/*", {
            cwd: LocalRepoPath,
            nodir: true,
            ignore: IGNORE_PATTERNS,
        });

        console.log(`Found ${files.length} files`);

        for (const file of files) {
            const fullFilePath = path.join(LocalRepoPath, file);
            const content = fs.readFileSync(fullFilePath, "utf-8");

            if (content.length > 1000000) continue;

            const storagePath = `${repoId}/${file}`;
            const { error: uploadError } = await supabase.storage.from("repos").upload(storagePath, content, {
                contentType: "text/plain",
                upsert: true
            });

            if (uploadError) {
                console.log("Error uploading file");

                console.log(uploadError);
                return { error: uploadError }
            }
            await supabase.from("files").insert({
                repo_id: repoId,
                path: "root/" + file,
                storage_path: storagePath
            })
        }
        return { success: true }
    } catch (e) {
        console.log(e);
        return { error: e }
    }
}