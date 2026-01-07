export interface Post {
  id: string;
  title: string;
  preview: string;
  name?: string;
}

export interface County {
  name: string;
  posts: Post[];
}

export const oregonCounties: County[] = [
  { name: 'Baker', posts: [] },
  { name: 'Benton', posts: [] },
  { name: 'Clackamas', posts: [] },
  { name: 'Clatsop', posts: [] },
  { name: 'Columbia', posts: [] },
  { name: 'Coos', posts: [] },
  { name: 'Crook', posts: [] },
  { name: 'Curry', posts: [] },
  { name: 'Deschutes', posts: [] },
  { name: 'Douglas', posts: [] },
  { name: 'Gilliam', posts: [] },
  { name: 'Grant', posts: [] },
  { name: 'Harney', posts: [] },
  { name: 'Hood River', posts: [] },
  { name: 'Jackson', posts: [] },
  { name: 'Jefferson', posts: [] },
  { name: 'Josephine', posts: [] },
  { name: 'Klamath', posts: [] },
  { name: 'Lake', posts: [] },
  { name: 'Lane', posts: [] },
  { name: 'Lincoln', posts: [] },
  { name: 'Linn', posts: [] },
  { name: 'Malheur', posts: [] },
  { name: 'Marion', posts: [] },
  { name: 'Morrow', posts: [] },
  { name: 'Multnomah', posts: [] },
  { name: 'Polk', posts: [] },
  { name: 'Sherman', posts: [] },
  { name: 'Tillamook', posts: [] },
  { name: 'Umatilla', posts: [] },
  { name: 'Union', posts: [] },
  { name: 'Wallowa', posts: [] },
  { name: 'Wasco', posts: [] },
  { name: 'Washington', posts: [] },
  { name: 'Wheeler', posts: [] },
  { name: 'Yamhill', posts: [] },
];
