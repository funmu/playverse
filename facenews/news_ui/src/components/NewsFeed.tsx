'use client';

import { useState } from 'react';
import { useNews } from '@/hooks/useNews';
import { NewsItem } from '@/components/NewsItem';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Grid2X2, List } from 'lucide-react';

type ViewMode = 'grid' | 'list';
type SortOrder = 'newest' | 'oldest';

export function NewsFeed() {
  const { news, isLoading, error } = useNews();
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [sortOrder, setSortOrder] = useState<SortOrder>('newest');

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  const sortedNews = [...news].sort((a, b) => {
    const dateA = new Date(a.publishedAt).getTime();
    const dateB = new Date(b.publishedAt).getTime();
    return sortOrder === 'newest' ? dateB - dateA : dateA - dateB;
  });

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <div className="flex space-x-2">
          <Button
            variant={viewMode === 'grid' ? 'default' : 'outline'}
            onClick={() => setViewMode('grid')}
          >
            <Grid2X2 className="mr-2 h-4 w-4" /> Grid
          </Button>
          <Button
            variant={viewMode === 'list' ? 'default' : 'outline'}
            onClick={() => setViewMode('list')}
          >
            <List className="mr-2 h-4 w-4" /> List
          </Button>
        </div>
        <Select
          value={sortOrder}
          onValueChange={(value) => setSortOrder(value as SortOrder)}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="newest">Newest First</SelectItem>
            <SelectItem value="oldest">Oldest First</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className={`grid gap-6 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'}`}>
        {sortedNews && sortedNews.map((item) => (
          <NewsItem key={item.url} {...item} />
        ))}
      </div>
    </div>
  );
}

