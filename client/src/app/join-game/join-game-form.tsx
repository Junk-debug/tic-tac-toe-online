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
import { Label } from "@/components/ui/label";

const JoinGameForm = () => (
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
);

export default JoinGameForm;
