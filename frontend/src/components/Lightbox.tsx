import React from 'react'
import styled from 'styled-components'

const APP_BAR_HEIGHT = 64;

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
  z-index: 1000;
`;

const LightboxContent = styled.div`
  background: white;
  border-radius: 16px;
  max-width: 90vw;
  max-height: 90vh;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  overflow: auto;
`

interface LightboxProps {
  onClose: () => void
  children: React.ReactNode
}

export const Lightbox: React.FC<LightboxProps> = ({ onClose, children }) => {
  return (
    <DimmedBackground onClick={onClose}>
      <LightboxContent onClick={(e: any) => e.stopPropagation()}>
        {children}
      </LightboxContent>
    </DimmedBackground>
  )
}
