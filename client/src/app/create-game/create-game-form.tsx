"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

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
} from "./create-game-schema";

const defaultValues: CreateGameFormSchema = {
  playerName: "",
  fieldSize: "3x3",
};

const CreateGameForm = () => {
  const form = useForm<CreateGameFormSchema>({
    resolver: zodResolver(createGameFormSchema),
    defaultValues,
  });

  function onSubmit(values: CreateGameFormSchema) {
    console.log(values);
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
                    <SelectItem value="3x3">3x3</SelectItem>
                    <SelectItem value="5x5">5x5</SelectItem>
                    <SelectItem value="9x9">9x9</SelectItem>
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
