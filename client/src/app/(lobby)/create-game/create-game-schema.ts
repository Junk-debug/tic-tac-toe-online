import { z } from "zod";

export enum FieldSize {
  "3x3" = "3x3",
  "5x5" = "5x5",
  "9x9" = "9x9",
}

export const createGameFormSchema = z.object({
  playerName: z.string().min(2).max(50),
  fieldSize: z.nativeEnum(FieldSize),
});

export type CreateGameFormSchema = z.infer<typeof createGameFormSchema>;
