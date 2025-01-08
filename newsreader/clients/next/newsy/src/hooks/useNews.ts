import { useState, useEffect } from 'react';

interface NewsItem {
  source: {
    id: string;
    name: string;
  };
  author: string;
  title: string;
  description: string;
  url: string;
  urlToImage: string;
  publishedAt: string;
  content: string;
}

interface NewsResponse {
  status: string;
  totalResults: number;
  articles: NewsItem[];
}

export function useNews() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchNews() {
      try {
        const response = await fetch('/api/news');
        if (!response.ok) {
          throw new Error('Failed to fetch news');
        }
        console.info('Fetching ...');
        const data: NewsResponse = await response.json();
        // console.info('News: ', data?.result)
        const filteredData = data?.result?.articles?.filter(i => i?.title !== '[Removed]');
        setNews(filteredData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    }

    fetchNews();
  }, []);

  return { news, isLoading, error };
}

