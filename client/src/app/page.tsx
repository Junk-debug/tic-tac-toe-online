import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import CreateGameForm from "./create-game/create-game-form";
import JoinGameForm from "./join-game/join-game-form";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      {/* <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight md:text-5xl mb-6 mt-40">
        Tic Tac Toe Online
      </h1> */}
      <Tabs defaultValue="create-game" className="w-[300px] sm:w-[400px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="create-game">Create</TabsTrigger>
          <TabsTrigger value="join-game">Join</TabsTrigger>
        </TabsList>
        <TabsContent value="create-game">
          <CreateGameForm />
        </TabsContent>
        <TabsContent value="join-game">
          <JoinGameForm />
        </TabsContent>
      </Tabs>
    </main>
  );
}
