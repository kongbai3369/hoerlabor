/**
 * 音频外链解析器 (Audio URL Resolver)：
 * - 本地开发模式：通过 VITE_AUDIO_BASE_URL (如 http://localhost:8080/audio) 读取 D 盘 Range 服务
 * - 生产上线模式：通过 VITE_AUDIO_BASE_URL (如 Cloudflare R2 / AWS S3 CDN 域名) 串流分发
 * - 绝对不将上百兆音频直接打进 Cloudflare Pages 构建包
 */
export function resolveAudioUrl(path: string | null | undefined): string {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path;
  }
  const baseUrl = import.meta.env.VITE_AUDIO_BASE_URL || '';
  if (!baseUrl) {
    return path;
  }
  const cleanBase = baseUrl.replace(/\/+$/, '');
  const cleanPath = path.replace(/^\/+/, '');
  return `${cleanBase}/${cleanPath}`;
}
