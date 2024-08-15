import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectValue,
  SelectTrigger,
} from "@/components/ui/select";

const CreateGameForm = () => (
  <TabsContent value="create-game">
    <Card>
      <CardHeader>
        <CardTitle>Create a game</CardTitle>
        <CardDescription>
          Create a new game and invite your friends
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="space-y-1">
          <Label htmlFor="playerName">Player name</Label>
          <Input placeholder="John Doe" id="playerName" />
        </div>

        <div className="space-y-1">
          <Label htmlFor="playerName">Field size</Label>
          <Select defaultValue="3x3">
            <SelectTrigger>
              <SelectValue placeholder="Select field size" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="3x3">3x3</SelectItem>
              <SelectItem value="5x5">5x5</SelectItem>
              <SelectItem value="9x9">9x9</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* player name */}
        {/* field size */}
        {/* players count size */}

        {/*
        <div className="space-y-1">
          <Label htmlFor="username">Username</Label>
          <Input id="username" defaultValue="@peduarte" />
        </div> */}
      </CardContent>
      <CardFooter>
        <Button>Create</Button>
      </CardFooter>
    </Card>
  </TabsContent>
);

const JoinGameForm = () => (
  <TabsContent value="join-game">
    <Card>
      <CardHeader>
        <CardTitle>Join the game</CardTitle>
        <CardDescription>Join an existing game</CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="space-y-1">
          <Label htmlFor="playerName">Player name</Label>
          <Input placeholder="Albert Einstein" id="playerName" />
        </div>
        <div className="space-y-1">
          <Label htmlFor="key">Game key</Label>
          <Input id="key" placeholder="123456789" />
        </div>
      </CardContent>
      <CardFooter>
        <Button>Join</Button>
      </CardFooter>
    </Card>
  </TabsContent>
);

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-4">
      <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight md:text-5xl mb-6 mt-40">
        Tic Tac Toe Online
      </h1>
      <Tabs defaultValue="create-game" className="w-[300px] sm:w-[400px]">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="create-game">Create</TabsTrigger>
          <TabsTrigger value="join-game">Join</TabsTrigger>
        </TabsList>
        <CreateGameForm />
        <JoinGameForm />
      </Tabs>
    </main>
  );
}
