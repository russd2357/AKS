import React from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageBlogCards from '@site/src/components/HomepageFeatures';
import { JSX } from 'react';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">Azure Kubernetes Service Engineering Blog</p>
        <div className={styles.heroDescription}>
          <p>
            Welcome to the official AKS Engineering Blog. Here, we share insights, best practices, 
            and deep dives into Azure Kubernetes Service from the team that builds it.
          </p>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home`}
      description="Azure Kubernetes Service Engineering Blog - Technical insights, best practices, and deep dives from the AKS team">
      <HomepageHeader />
      <main>
        <HomepageBlogCards />
      </main>
    </Layout>
  );
}