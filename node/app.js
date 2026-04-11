import express from "express";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";
import repoRoute from "./routes/repo.js";
import { glob } from "glob";
import { nanoid } from "nanoid";
import simpleGit from "simple-git";

dotenv.config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);
const app = express();
const port = 8080;

app.get("/", (req, res) => {
    res.send("Hello World!");
});

app.use("/api/repo", repoRoute)

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});