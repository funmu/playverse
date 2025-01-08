import { NewsFeed } from '@/components/NewsFeed';

export default function Home() {
  return (
    <main className="container mx-auto py-8">
      <h1 className="text-4xl font-bold mb-8">Newsy</h1>
      <NewsFeed />
    </main>
  );
}

