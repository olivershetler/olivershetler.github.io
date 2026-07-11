export interface Talk {
  title: string;
  event: string;
  location: string;
  date: string;   // display string
  href: string;
  blurb: string;
  animation?: {
    src: string;
    poster?: string;
    caption: string;
  };
}

export const talks: Talk[] = [
  {
    title: 'From Medical Codes to Cash and Coverage: Risk-Filtered Insurance Claims Automation',
    event: 'Machine Learning Week US 2026',
    location: 'San Francisco',
    date: 'May 2026',
    href: 'https://machinelearningweek.com/agenda/2026/',
    blurb: 'Why AI medical coding automation so often misses its expected ROI in production, and how pairing it with risk-filtered review concentrates human coders where the financial impact is greatest.',
    animation: {
      src: '/media/talks/risk-filtered-automation.mp4',
      poster: '/media/talks/risk-filtered-automation.png',
      caption: 'Schematic of the talk\'s simulation: routing claims by predicted denial risk, automating the low-risk majority and sending the risky tail to human review, cuts cost by roughly half while holding the failure rate at the human baseline.',
    },
  },
];
