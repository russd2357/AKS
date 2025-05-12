import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import BlogListPaginator from '@theme/BlogListPaginator';
import { ThemeClassNames } from '@docusaurus/theme-common';
import clsx from 'clsx';
import styles from './styles.module.css';

// Azure recommended blog card component following Azure design patterns
export default function BlogListPage(props) {
  const { metadata, items, sidebar } = props;
  
  // Function to organize posts by year
  const renderSidebarByYear = () => {
    // If sidebar data doesn't exist, return null
    if (!sidebar || !sidebar.items) {
      return null;
    }
    
    // Process sidebar data to extract years and posts
    const postsByYear = {};
    
    // Helper function to process items recursively and extract years
    const processItems = (items) => {
      if (!items || !Array.isArray(items)) {
        return;
      }
      
      items.forEach(item => {
        // If the item has a permalink, it's a post
        if (item.permalink) {
          // Extract year from permalink (assumes format /blog/YYYY/MM/DD/slug or /blog/YYYY-MM-DD-slug)
          const yearMatch = item.permalink.match(/\/blog\/(\d{4})/);
          const year = yearMatch ? yearMatch[1] : 'Other';
          
          // Initialize year array if it doesn't exist
          if (!postsByYear[year]) {
            postsByYear[year] = [];
          }
          
          // Add post to the appropriate year
          postsByYear[year].push(item);
        }
        // If the item has nested items, process them recursively
        else if (item.items && Array.isArray(item.items)) {
          processItems(item.items);
        }
      });
    };
    
    // Process all sidebar items
    processItems(sidebar.items);
    
    // Get years and sort them in descending order (newest first)
    const years = Object.keys(postsByYear).sort((a, b) => b.localeCompare(a));
    
    return (
      <div className={styles.sidebarYears}>
        <h3 className={styles.sidebarHeading}>{sidebar.title || 'Blog Posts'}</h3>
        
        {years.map(year => (
          <div key={year} className={styles.yearGroup}>
            <h4 className={styles.yearHeading}>{year}</h4>
            <ul className={styles.postList}>
              {postsByYear[year].map((post, index) => (
                <li key={index} className={styles.postItem}>
                  <Link 
                    to={post.permalink}
                    className={styles.postLink}
                  >
                    {post.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    );
  };
  
  return (
    <Layout
      title={metadata.blogTitle}
      description={metadata.blogDescription}
      wrapperClassName={ThemeClassNames.wrapper.blogPages}>
      <div className="container margin-top--lg">
        <div className="row">
          {/* Custom sidebar implementation with year-based grouping */}
          <div className={clsx('col col--4', styles.sidebarColumn)}>
            {renderSidebarByYear()}
          </div>
          
          {/* Main content column with blog cards - unchanged */}
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