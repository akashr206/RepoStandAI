import simpleGit from "simple-git";
import path from "path";
import fs from "fs";

const cloneRepo = async (repoUrl, repoPath) => {
    try {
        fs.mkdirSync(path.dirname(repoPath), { recursive: true });
        const git = simpleGit();
        await git.clone(repoUrl, repoPath);
        return { success: true }
    } catch (error) {
        return { error }
    }

}

export { cloneRepo };