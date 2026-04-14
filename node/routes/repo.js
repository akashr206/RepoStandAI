import express from "express";
import { processRepo } from "../services/process.js";
import { nanoid } from "nanoid";
import { createClient } from "@supabase/supabase-js";

const route = express.Router();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

route.post('/ingest', async (req, res) => {
    try {
        const { repoUrl } = req.body;
        if (!repoUrl) {
            return res.status(400).json({ error: "Repository URL is required" })
        }
        const repoId = nanoid(10);
        const repoName = repoUrl
            .split("/")
            .filter(Boolean)
            .pop()
            .replace(".git", "");
        
        await supabase.from("repos").insert({
            id: repoId,
            name: repoName,
            status: "processing"
        })
        res.json({ status: "processing", repoId })
        processRepo(repoUrl, repoId);
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: "Internal server error" })
    }
})

route.get('/status/:repoId', async (req, res) => {
    try {
        const { repoId } = req.params;
        const { data, error } = await supabase.from("repos").select("status").eq("id", repoId);
        if (error) {
            return res.status(500).json({ error: "Internal server error" })
        }
        res.json(data);
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: "Internal server error" })
    }
})
export default route;