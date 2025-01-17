import Image from 'next/image';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { formatDate } from '@/utils/formatDate';

interface NewsItemProps {
  title: string;
  description: string;
  author: string;
  publishedAt: string;
  url: string;
  urlToImage: string;
}

export function NewsItem({ title, description, author, publishedAt, url, urlToImage }: NewsItemProps) {
  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="line-clamp-2">{title}</CardTitle>
      </CardHeader>
      <CardContent className="flex-grow">
        {urlToImage && (
          <div className="relative w-full h-48 mb-4">
            <Image
              src={urlToImage}
              alt={title}
              fill
              className="object-cover rounded-md"
            />
          </div>
        )}
        <p className="line-clamp-3">{description}</p>
      </CardContent>
      <CardFooter className="flex justify-between items-center">
        <div className="text-sm text-muted-foreground">
          {author && <p>By {author}</p>}
          <p>{formatDate(publishedAt)}</p>
        </div>
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary hover:underline"
        >
          Read more
        </a>
      </CardFooter>
    </Card>
  );
}

