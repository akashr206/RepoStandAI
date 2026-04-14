import path from "path";
import dotenv from "dotenv";
import fs from "fs";
import { cloneRepo } from "./git.js";
import { storeRepo } from "./storage.js";
import { createClient } from "@supabase/supabase-js";
import { embedFile } from "./embedding.js";
dotenv.config();

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

export async function processRepo(repoUrl, repoId) {
    try {
        const repoPath = path.join(process.cwd(), 'repos', repoId);
        let result = await cloneRepo(repoUrl, repoPath);
        if (result.error) {
            console.log("error cloning");
            await supabase.from("repos").update({ status: "failed" }).eq("id", repoId);
            return;
        }
        console.log("cloned.");

        // result = await storeRepo(repoPath, repoId);
        // if (result.error) {
        //     console.log("error");
        //     await supabase.from("repos").update({ status: "failed" }).eq("id", repoId);
        //     await fs.promises.rm(repoPath, { recursive: true, force: true });
        //     console.log("deleted");
        //     return;
        // }
        console.log("stored.");
        result = await embedFile(repoPath, repoId);
        if (result.error) {
            console.log("error");
            await supabase.from("repos").update({ status: "failed" }).eq("id", repoId);
            await fs.promises.rm(repoPath, { recursive: true, force: true });
            console.log("deleted");
            return;
        }
        console.log("embedded.");
        await fs.promises.rm(repoPath, { recursive: true, force: true });
        console.log("deleted");

        await supabase.from("repos").update({ status: "success" }).eq("id", repoId);

    } catch (error) {
        console.log(error);
        const repoPath = path.join(process.cwd(), 'repos', repoId);
        await supabase.from("repos").update({ status: "failed" }).eq("id", repoId);
        await fs.promises.rm(repoPath, { recursive: true, force: true });
        console.log("deleted");
        return { error: error }
    }
}