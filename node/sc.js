import { embed } from "./util/embed.js";

const { embeddings } = await embed(["hello world"]);
console.log(embeddings);