import { FC, ReactNode, useEffect } from 'react'
import styled from 'styled-components'
import { ZIndex } from '../constants';
import { APP_BAR_HEIGHT } from './Header';

const DimmedBackground = styled.div`
  position: fixed;
  top: ${APP_BAR_HEIGHT}px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: ${ZIndex.LIGHT_BOX};
`;

const LightboxContent = styled.div`
  background: white;
  border-radius: 16px;
  max-width: 90vw;
  max-height: 90vh;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
  overflow-x: hidden;
`;

interface LightboxProps {
  onClose: () => void
  children: ReactNode
}

export const Lightbox: FC<LightboxProps> = ({ onClose, children }) => {
  // Disable body scroll when lightbox is open
  useEffect(() => {
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = originalOverflow;
    };
  }, []);

  return (
    <DimmedBackground onClick={onClose}>
      <LightboxContent onClick={(e: any) => e.stopPropagation()}>
        {children}
      </LightboxContent>
    </DimmedBackground>
  )
}
