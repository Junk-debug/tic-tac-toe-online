import { create } from "zustand";

interface GameState {
  field: number[][] | null;
  playerName: string | null;
  key: number | null;
  currentMove: string | null;
  updateGameState: (
    data: Omit<
      GameState,
      "updateGameState" | "updateField" | "updateCurrentMove"
    >,
  ) => void;
  updateField: (data: number[][] | null) => void;
  updateCurrentMove: (data: string | null) => void;
}

export const useGameStore = create<GameState>()((set) => ({
  playerName: null,
  field: null,
  key: null,
  currentMove: null,
  updateGameState: (data) => set(data),
  updateField: (data) => set((state) => ({ ...state, field: data })),
  updateCurrentMove: (data) =>
    set((state) => ({ ...state, currentMove: data })),
}));
