// Optional animation shape: { src, poster?, caption }. Set animation.src to a path under
// /media/pubs/<slug>.mp4, with animation.poster when needed, to render a clip below the paper.
export interface Publication {
  authors: string;
  title: string;
  venue: string;
  year: number;
  note?: string;
  peerReviewed?: boolean;
  animation?: {
    src: string;
    poster?: string;
    caption: string;
  };
  href: string;
}

export const publications: Publication[] = [
  {
    authors: 'Aoun A*, Shetler O*, Raghuraman R, Rodriguez GA, Hussaini SA',
    title:
      'Beyond Correlation: Optimal Transport Metrics for Characterizing Representational Stability and Remapping in Neurons Encoding Spatial Memory',
    venue: 'Frontiers in Cellular Neuroscience',
    year: 2024,
    note: '*co-first author',
    peerReviewed: true,
    animation: {
      src: '/media/pubs/beyond-correlation.mp4',
      poster: '/media/pubs/beyond-correlation.png',
      caption:
        'Schematic: optimal transport distance keeps measuring spatial change where correlation goes blind.',
    },
    href: 'https://doi.org/10.3389/fncel.2023.1273283',
  },
  {
    authors:
      'Rodriguez GA, Rothenberg EF, Shetler CO, Aoun A, Posani L, Vajram SV, Tedesco T, Fusi S, Hussaini SA',
    title:
      'Impaired Spatial Coding and Neuronal Hyperactivity in the Medial Entorhinal Cortex of Aged AppNL-G-F Mice',
    venue: 'bioRxiv',
    year: 2024,
    animation: {
      src: '/media/pubs/mec-spatial-coding.mp4',
      poster: '/media/pubs/mec-spatial-coding.png',
      caption:
        "Schematic: in the Alzheimer's model the entorhinal grid degrades and baseline firing rises; an optimal-transport stability score against a chance reference shows the degraded maps sit at chance (disordered) while healthy maps stay far more stable.",
    },
    href: 'https://doi.org/10.1101/2024.11.26.624990',
  },
  {
    authors: 'Raghuraman R, Aoun A, Herman M, Shetler O, Nahmani E, Hussaini SA',
    title: "Lateral Entorhinal Cortex Dysfunction in Alzheimer's Disease Mice",
    venue: 'bioRxiv',
    year: 2024,
    animation: {
      src: '/media/pubs/lec-dysfunction.mp4',
      poster: '/media/pubs/lec-dysfunction.png',
      caption: 'Schematic: the lateral entorhinal cortex tags objects; in disease the tag blurs.',
    },
    href: 'https://doi.org/10.1101/2024.04.15.589589',
  },
  {
    authors: 'Barrett GM*, Vajram S*, Shetler O, Aoun A, Hussaini SA',
    title: 'Open-Source Tools to Analyze Temporal and Spatial Properties of Local Field Potentials',
    venue: 'bioRxiv',
    year: 2024,
    note: '*co-first author',
    animation: {
      src: '/media/pubs/lfp-tools.mp4',
      poster: '/media/pubs/lfp-tools.png',
      caption:
        'Schematic: hfoGUI reads ripples in time; the Spatial Spectral Mapper reads power across space.',
    },
    href: 'https://doi.org/10.1101/2024.03.14.584529',
  },
  {
    authors: 'Vázquez-Abad FJ, Shetler O, Soto P',
    title: 'Quantile Formulation for Optimization Under a Qualitative Risk Constraint',
    venue: 'IEEE Conference on Decision and Control',
    year: 2022,
    peerReviewed: true,
    animation: {
      src: '/media/pubs/quantile-risk.mp4',
      poster: '/media/pubs/quantile-risk.png',
      caption:
        "Schematic: an optimizer improves its objective while keeping the 2D outcome distribution's confidence ellipse inside the risk boundary (probability of failure within budget).",
    },
    href: 'https://doi.org/10.1109/CDC51059.2022.9992955',
  },
];
