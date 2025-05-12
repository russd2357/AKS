import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import BlogListPaginator from '@theme/BlogListPaginator';
import BlogSidebar from '@theme/BlogSidebar';
import { ThemeClassNames } from '@docusaurus/theme-common';
import clsx from 'clsx';
import styles from './styles.module.css';

// Azure recommended blog card component following Azure design patterns
export default function BlogListPage(props) {
  const { metadata, items, sidebar } = props;
  
  return (
    <Layout
      title={metadata.blogTitle}
      description={metadata.blogDescription}
      wrapperClassName={ThemeClassNames.wrapper.blogPages}>
      <div className="container margin-top--lg">
        <div className="row">
          {/* Proper sidebar width following Azure documentation standards */}
          <div className={clsx('col col--4', styles.sidebarColumn)}>
            <BlogSidebar sidebar={sidebar} />
          </div>
          
          {/* Main content column with blog cards - adjusted for better balance */}
          <div className="col col--8">
            <div className={styles.blogListGrid}>
              {items.map(({content: BlogPostContent}) => {
                const {metadata: blogMetadata, frontMatter} = BlogPostContent;
                const {title, permalink, description, date, formattedDate, tags, authors} = blogMetadata;
                
                return (
                  <div key={permalink} className={styles.blogCard}>
                    <div className={clsx('card', styles.card)}>
                      {frontMatter.image && (
                        <div className={styles.cardImage}>
                          <img 
                            src={frontMatter.image} 
                            alt={title}
                          />
                        </div>
                      )}
                      <div className="card__header">
                        <h3>{title}</h3>
                      </div>
                      <div className="card__body">
                        <p>{description}</p>
                      </div>
                      <div className="card__footer">
                        <div className={styles.cardMeta}>
                          <span className={styles.cardDate}>{formattedDate}</span>
                          {authors && authors.length > 0 && (
                            <span className={styles.cardAuthor}>
                              by {authors[0].name}
                            </span>
                          )}
                        </div>
                        <Link
                          to={permalink}
                          className="button button--primary button--sm">
                          Read More
                        </Link>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
            <BlogListPaginator metadata={metadata} />
          </div>
        </div>
      </div>
    </Layout>
  );
}