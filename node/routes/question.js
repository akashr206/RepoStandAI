import express from "express";
import { createClient } from "@supabase/supabase-js";
import { embed } from "../util/embed.js";
const route = express.Router();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

route.post("/", async (req, res) => {
    try {
        const { repoId, question } = req.body;
        if (!repoId || !question) {
            return res.status(400).json({ error: "Repository ID and question are required" })
        }
        let { data, error } = await supabase.from("repos").select("status").eq("id", repoId);
        
        
        if (data[0].status != "success") {
            return res.status(400).json({ error: "Repository is not ready yet" })
        }
        if (error) {
            return res.status(500).json({ error: "Internal server error" })
        }
        const embedding = await embed(question);
        if (embedding.error) {
            return res.status(500).json({ error: "Internal server error" })
        }
        let { data: top_chunks, error: e } = await supabase.rpc("match_embeddings", {
            query_embedding: embedding.embeddings[0],
            match_count: 10,
            repo_id_input: repoId
        });

        if (e) {
            console.error(e);
        }

        res.json({ top_chunks })

    } catch (error) {
        console.log(error);
        res.status(500).json({ error: "Internal server error" })
    }
})
export default route;