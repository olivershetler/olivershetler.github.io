export interface Project {
  title: string;
  blurb: string;
  tags: string[];
  repo: string;
  pdf?: string;
}

export const projects: Project[] = [
  {
    title: 'Neural spike train profiling',
    blurb:
      "Profiling neural spike trains from a cat's visual cortex with multinomial regression and discriminant analysis.",
    tags: ['R', 'statistics'],
    repo: 'https://github.com/olivershetler/cat-cortex/',
    pdf: 'https://github.com/olivershetler/cat-cortex/raw/main/article.pdf',
  },
  {
    title: 'Seizure detection',
    blurb: 'Detecting seizures in EEG time series with feature extraction and classical classifiers.',
    tags: ['Python', 'time series'],
    repo: 'https://github.com/olivershetler/seizures/',
    pdf: 'https://github.com/olivershetler/seizures/raw/main/article.pdf',
  },
  {
    title: 'Grip force from biosignals',
    blurb:
      'Predicting human grip force from EEG, fNIRS, and EMG data with deep transfer learning.',
    tags: ['Keras', 'deep learning'],
    repo: 'https://github.com/olivershetler/hygrip/',
    pdf: 'https://github.com/olivershetler/hygrip/raw/main/article.pdf',
  },
  {
    title: 'Tumor detection',
    blurb: 'Tumor detection in medical images with CNN transfer learning.',
    tags: ['Keras', 'computer vision'],
    repo: 'https://github.com/olivershetler/tumors/',
    pdf: 'https://github.com/olivershetler/tumors/raw/main/article.pdf',
  },
  {
    title: 'NYC PLUTO research database',
    blurb:
      'A research-oriented Postgres database engineered from NYC Open Data PLUTO datasets.',
    tags: ['SQL', 'data engineering'],
    repo: 'https://github.com/olivershetler/pluto-database/',
    pdf: 'https://github.com/olivershetler/pluto-database/blob/main/guides/article.pdf',
  },
  {
    title: 'Lease renewal modeling',
    blurb: 'Predicting NYC lease renewal terms from PLUTO panel data.',
    tags: ['Python', 'statistics'],
    repo: 'https://github.com/olivershetler/pluto-modeling/',
    pdf: 'https://github.com/olivershetler/pluto-modeling/raw/main/article.pdf',
  },
];
