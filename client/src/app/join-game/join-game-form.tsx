"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

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

const defaultValues: JoinGameFormSchema = {
  playerName: "",
  key: "",
};

const JoinGameForm = () => {
  const form = useForm<JoinGameFormSchema>({
    resolver: zodResolver(joinGameFormSchema),
    defaultValues,
  });

  const onSubmit = (values: JoinGameFormSchema) => {
    console.log(values);
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
