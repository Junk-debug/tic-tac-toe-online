import { z } from "zod";

export const createGameFormSchema = z.object({
  playerName: z.string().min(2).max(50),
  fieldSize: z.enum(["3x3", "5x5", "9x9"]),
});

export type CreateGameFormSchema = z.infer<typeof createGameFormSchema>;
