import express from "express";
import { simpleGit } from "simple-git";
import path from "path";
import fs from "fs";

const route = express.Router();

route.post('/', async (req, res) => {
    try {
        const { repoUrl } = req.body;

        if (!repoUrl) {
            return res.status(400).json({ error: "Repository URL is required" })
        }
        const repoName = repoUrl.split('/').pop().replace('.git', '');
        const repoPath = path.join(process.cwd(), 'repos', repoName + "-" + Date.now());

        fs.mkdirSync(path.dirname(repoPath), { recursive: true });

        const git = simpleGit();

        await git.clone(repoUrl, repoPath);

        res.json({ message: "Repository cloned successfully", repoPath })

    } catch (error) {
        console.log(error);
        res.status(500).json({ error: "Internal server error" })
    }
})


export default route