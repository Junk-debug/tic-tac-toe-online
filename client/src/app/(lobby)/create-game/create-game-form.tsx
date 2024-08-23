"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectValue,
  SelectTrigger,
} from "@/components/ui/select";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import {
  CreateGameFormSchema,
  createGameFormSchema,
  FieldSize,
} from "./create-game-schema";
import { useGameStore } from "@/app/game-store";

const defaultValues: CreateGameFormSchema = {
  playerName: "",
  fieldSize: FieldSize["3x3"],
};

type CreateGameDto = {
  all_players: number;
  player_name: string;
  player_first: 0 | 1 | 2;
  size_x: number;
  size_y: number;
  condition_win: number;
};

type CreateGameResponse = {
  data: {
    key: number;
    game_floor: number[][];
    now_move: string | null;
  };
  result: string;
  result_msg: string;
};

const createGame = async (params: CreateGameDto) => {
  const res = await fetch("http://localhost:8000/lobby/create_game", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
  });

  const data: CreateGameResponse = await res.json();
  return data;
};

const CreateGameForm = () => {
  const router = useRouter();

  const updateGameState = useGameStore((state) => state.updateGameState);

  const form = useForm<CreateGameFormSchema>({
    resolver: zodResolver(createGameFormSchema),
    defaultValues,
  });

  async function onSubmit(values: CreateGameFormSchema) {
    const res = await createGame({
      all_players: 2,
      player_name: values.playerName,
      player_first: 0,
      size_x: Number(values.fieldSize[0]),
      size_y: Number(values.fieldSize[0]),
      condition_win: 3,
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
  }

  const { handleSubmit, control } = form;

  return (
    <Form {...form}>
      <Card>
        <CardHeader>
          <CardTitle>Create a game</CardTitle>
          <CardDescription>
            Create a new game and invite your friends
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <FormField
            control={control}
            name="playerName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Player name</FormLabel>
                <FormControl>
                  <Input placeholder="John Doe" {...field} />
                </FormControl>
                <FormDescription>
                  This is your public display name.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="fieldSize"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Field size</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  defaultValue={field.value}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select field size" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {Object.entries(FieldSize).map(([key, value]) => (
                      <SelectItem key={key} value={value}>
                        {value}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FormDescription>Select the size of the field</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        </CardContent>
        <CardFooter>
          <Button className="w-full" onClick={handleSubmit(onSubmit)}>
            Create
          </Button>
        </CardFooter>
      </Card>
    </Form>
  );
};

export default CreateGameForm;
