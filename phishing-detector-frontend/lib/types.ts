export interface CheckResult {
  url: string;
  is_phishing: boolean;
  confidence: number;
  similar_to: string | null;
  screenshot_url: string;
  original_screenshot_url: string | null;
  scores: {
    phash: number;
    ssim: number;
    cnn: number;
  };
  checked_at: string;
}
