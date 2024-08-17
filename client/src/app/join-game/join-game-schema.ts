import { z } from "zod";

export const joinGameFormSchema = z.object({
  playerName: z.string().min(2).max(50),
  key: z.string(),
});

export type JoinGameFormSchema = z.infer<typeof joinGameFormSchema>;
