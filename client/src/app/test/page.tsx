/* eslint-disable react/no-array-index-key */

"use client";

import { useEffect, useRef } from "react";
import { useGameStore } from "../game-store";

type MessageDto = {
  player_name: string;
  cell_col: number;
  cell_row: number;
};

const calculateSymbol = (cell: number) => {
  switch (cell) {
    case 1:
      return "X";
    case 2:
      return "O";
    default:
      return null;
  }
};

type GameResponse = {
  data: {
    game_floor: number[][];
    now_move: string | null;
  };
  result: string;
  result_msg: string;
};

export default function Page() {
  const gameKey = useGameStore((state) => state.key) || 0;
  const field = useGameStore((state) => state.field);
  const playerName = useGameStore((state) => state.playerName) || "";
  const currentMove = useGameStore((state) => state.currentMove);
  const updateField = useGameStore((state) => state.updateField);
  const updateCurrentMove = useGameStore((state) => state.updateCurrentMove);

  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(`ws://localhost:8000/room/ws/${gameKey}`);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("connected");
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onmessage = (event) => {
      const data: GameResponse | string = JSON.parse(event.data);
      console.log("Received message from server:", data);

      if (typeof data === "string") {
        console.log(data);
        return;
      }

      updateField(data.data.game_floor);
      updateCurrentMove(data.data.now_move);
    };

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gameKey]);

  const handleMove = (row: number, col: number) => {
    const message: MessageDto = {
      player_name: playerName,
      cell_col: col,
      cell_row: row,
    };

    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(message));
    } else {
      console.error("WebSocket not open");
    }
  };

  return (
    <div className="flex flex-col gap-1">
      <span>Game</span>
      <span>Current move: {currentMove}</span>
      <div>
        {field?.map((row, rowIndex) => (
          <div key={rowIndex} className="flex">
            {row.map((cell, cellIndex) => (
              <button
                type="button"
                onClick={() => handleMove(rowIndex, cellIndex)}
                key={cellIndex}
                className="w-10 h-10 border border-black flex items-center justify-center"
              >
                {calculateSymbol(cell)}
              </button>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
