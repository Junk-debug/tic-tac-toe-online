import { redirect } from "next/navigation";
import Link from "next/link";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import CreateGameForm from "@/app/(lobby)/create-game/create-game-form";
import JoinGameForm from "@/app/(lobby)/join-game/join-game-form";

type Props = {
  params: { lobbySlug: "create-game" | "join-game" | string };
};

export async function generateMetadata({ params: { lobbySlug } }: Props) {
  if (!["create-game", "join-game"].includes(lobbySlug)) {
    return {};
  }

  return {
    title: lobbySlug === "create-game" ? "Create Game" : "Join Game",
  };
}

export default function Home({ params: { lobbySlug } }: Props) {
  if (!["create-game", "join-game"].includes(lobbySlug)) {
    redirect("/create-game");
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      {/* <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight md:text-5xl mb-6 mt-40">
        Tic Tac Toe Online
      </h1> */}
      <Tabs defaultValue={lobbySlug} className="w-[300px] sm:w-[400px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger asChild value="create-game">
            <Link href="/create-game">Create</Link>
          </TabsTrigger>
          <TabsTrigger asChild value="join-game">
            <Link href="/join-game">Join</Link>
          </TabsTrigger>
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
