import { InferenceClient } from "@huggingface/inference";
import dotenv from "dotenv";

dotenv.config();

const hf = new InferenceClient(process.env.HF_API_KEY);

export async function embed(text) {
    try {
        const response = await hf.featureExtraction({
            model: "BAAI/bge-base-en-v1.5",
            inputs: text,
        });

        return {
            success: true,
            embeddings: Array.isArray(response[0]) ? response : [response],
        };
    } catch (error) {
        console.log(error);
        return { error };
    }
}