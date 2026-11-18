import React from 'react';
import {
  Award,
  GraduationCap,
  Newspaper,
  Radio,
  Mic,
  Podcast,
  User,
} from 'lucide-react';
import type { ListeningTrack } from '../types/listening';
import { getSourceDisplayInfo } from '../types/listening';

interface SourceBadgeProps {
  track: Pick<ListeningTrack, 'source' | 'sourceCategory'>;
  compact?: boolean;
  className?: string;
}

export const SourceBadge: React.FC<SourceBadgeProps> = ({
  track,
  compact = false,
  className = '',
}) => {
  const info = getSourceDisplayInfo(track);

  const renderIcon = () => {
    const iconClass = compact ? 'w-3 h-3 shrink-0' : 'w-3.5 h-3.5 shrink-0';
    switch (info.iconKey) {
      case 'award':
        return <Award className={iconClass} />;
      case 'graduation':
        return <GraduationCap className={iconClass} />;
      case 'newspaper':
        return <Newspaper className={iconClass} />;
      case 'radio':
        return <Radio className={iconClass} />;
      case 'mic':
        return <Mic className={iconClass} />;
      case 'podcast':
        return <Podcast className={iconClass} />;
      default:
        return <User className={iconClass} />;
    }
  };

  return (
    <span
      className={`inline-flex items-center gap-1 border font-semibold ${
        compact
          ? 'text-[10px] px-1.5 py-0.5 rounded'
          : 'text-xs px-2.5 py-0.5 rounded-full'
      } ${info.badgeClass} ${className}`}
      title={info.label}
    >
      {renderIcon()}
      <span className="truncate max-w-[140px]">
        {compact ? info.shortLabel : info.label}
      </span>
    </span>
  );
};
