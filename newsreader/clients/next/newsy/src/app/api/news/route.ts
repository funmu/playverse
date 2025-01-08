import { NextResponse } from 'next/server';

export async function GET() {
  // In a real application, you would fetch this data from an external API

  const newsApiData = await fetch('http://localhost:8080/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    },
    body: JSON.stringify({
      operation: {
        name: 'latest',
        args: { scope: 'canada' }
      }
    })
  });
  const newsData = await newsApiData.json();
  // console.info(JSON.stringify(newsData))
  // const newsData = {
  //   "status": "ok",
  //   "totalResults": 1,
  //   "articles": [
  //     {
  //       "source": {
  //         "id": "business-insider",
  //         "name": "Business Insider"
  //       },
  //       "author": "Steven John",
  //       "title": "I tried roast-beef sandwiches from Jimmy John's, Subway, and Jersey Mike's. None were perfect, but one stood out.",
  //       "description": "I ordered a roast-beef sandwich from Subway, Jimmy John's, and Jersey Mike's to see which popular chain does the classic sub best. None wowed me.",
  //       "url": "https://www.businessinsider.com/which-chain-best-roast-beef-sandwich-subway-jimmy-johns-jersey-mikes",
  //       "urlToImage": "https://i.insider.com/67608cd9d0de6a4f27d3375d?width=1200&format=jpeg",
  //       "publishedAt": "2024-12-22T12:34:01Z",
  //       "content": "I compared roast-beef sandwiches from Subway, Jimmy John's, and Jersey Mike's.Steven John\r\n<ul><li>I compared roast-beef sandwiches at Jimmy John's, Jersey Mike's, and Subway to find the best one.</l… [+4687 chars]"
  //     }
  //   ]
  // };

  return NextResponse.json(newsData);
}

