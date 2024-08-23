"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import { joinGameFormSchema, JoinGameFormSchema } from "./join-game-schema";
import { useGameStore } from "@/app/game-store";

const defaultValues: JoinGameFormSchema = {
  playerName: "",
  key: "",
};

type JoinGameDto = {
  key: number;
  player_name: string;
};

type JoinGameResponse = {
  data: {
    key: number;
    game_floor: number[][];
    now_move: string | null;
  };
  result: string;
  result_msg: string;
};

const joinGame = async (params: JoinGameDto) => {
  const res = await fetch("http://localhost:8000/lobby/join_the_game", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
  });
  const data: JoinGameResponse = await res.json();
  return data;
};

const JoinGameForm = () => {
  const router = useRouter();
  const updateGameState = useGameStore((state) => state.updateGameState);

  const form = useForm<JoinGameFormSchema>({
    resolver: zodResolver(joinGameFormSchema),
    defaultValues,
  });

  const onSubmit = async (values: JoinGameFormSchema) => {
    console.log(values);

    const res = await joinGame({
      key: Number(values.key),
      player_name: values.playerName,
    });

    updateGameState({
      key: res.data.key,
      playerName: values.playerName,
      field: res.data.game_floor,
      currentMove: res.data.now_move,
    });

    console.log(res);
    console.log(res.data.key);

    router.push("/test");
  };

  const { handleSubmit, control } = form;

  return (
    <Form {...form}>
      <Card>
        <CardHeader>
          <CardTitle>Join the game</CardTitle>
          <CardDescription>Join an existing game</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <FormField
            control={control}
            name="playerName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Player name</FormLabel>
                <FormControl>
                  <Input placeholder="Albert Einstein" {...field} />
                </FormControl>
                <FormDescription>
                  This is your public display name.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={control}
            name="key"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Game key</FormLabel>
                <FormControl>
                  <Input placeholder="123456789" {...field} />
                </FormControl>
                <FormDescription>
                  The key of the game that you want to join.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        </CardContent>
        <CardFooter>
          <Button className="w-full" onClick={handleSubmit(onSubmit)}>
            Join
          </Button>
        </CardFooter>
      </Card>
    </Form>
  );
};

export default JoinGameForm;
