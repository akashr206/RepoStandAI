import express from "express";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";
import repoRoute from "./routes/repo.js";
import questionRoute from "./routes/question.js";


dotenv.config();
// const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);
const app = express();
const port = 8080;
app.use(express.json());
app.get("/", (req, res) => {
    res.send("Hello World!");
});

app.use("/api/repo", repoRoute)
app.use("/api/question", questionRoute)

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});