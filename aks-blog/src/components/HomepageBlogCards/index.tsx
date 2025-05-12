import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { usePluginData } from '@docusaurus/useGlobalData';
import { JSX } from 'react';
import styles from './styles.module.css';

type BlogPost = {
  id: string;
  metadata: {
    permalink: string;
    title: string;
    description: string;
    date: string;
    formattedDate: string;
    tags: Array<{ label: string; permalink: string }>;
    authors: Array<{ name: string; title: string; imageURL?: string }>;
  };
};

type BlogPluginData = {
  blogPosts: BlogPost[];
};

export default function HomepageBlogCards(): JSX.Element {
  // Access blog data using the usePluginData hook
  const { blogPosts } = usePluginData('docusaurus-plugin-content-blog', 'default') as BlogPluginData;

  // Take only the first 6 posts
  const recentPosts = blogPosts.slice(0, 6);

  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2 className={styles.sectionTitle}>Latest AKS Articles</h2>
          </div>
        </div>
        <div className="row">
          {recentPosts.map((post, idx) => (
            <div className="col col--4 margin-bottom--lg" key={idx}>
              <div className={clsx('card', styles.blogCard)}>
                <div className="card__image">
                  <img
                    src={`/img/blog-cards/${post.id.split('/').pop()}.png`}
                    alt={post.metadata.title}
                    onError={(e) => {
                      // Fallback to default image if the specific one doesn't exist
                      e.currentTarget.src = '/img/aks-blog-card-default.png';
                    }}
                  />
                </div>
                <div className="card__body">
                  <h3>{post.metadata.title}</h3>
                  <p>{post.metadata.description}</p>
                </div>
                <div className="card__footer">
                  <div className={styles.blogMeta}>
                    {post.metadata.authors?.length > 0 && (
                      <div className={styles.authorInfo}>
                        {post.metadata.authors[0].imageURL && (
                          <img 
                            src={post.metadata.authors[0].imageURL} 
                            alt={post.metadata.authors[0].name}
                            className={styles.authorAvatar}
                          />
                        )}
                        <span>{post.metadata.authors[0].name}</span>
                      </div>
                    )}
                    <span className={styles.blogDate}>{post.metadata.formattedDate}</span>
                  </div>
                  <Link
                    to={post.metadata.permalink}
                    className="button button--primary button--sm"
                  >
                    Read More
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="row">
          <div className="col col--12 text--center">
            <Link to="/archive" className="button button--secondary button--lg">
              View All Articles
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}