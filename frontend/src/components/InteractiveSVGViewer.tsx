import React, { useRef, useEffect, useState } from "react";
import { Box, IconButton, HStack, Text, VStack, Tooltip } from "@chakra-ui/react";

type InteractiveSVGViewerProps = {
  svgContent: string;
  title?: string;
};

const InteractiveSVGViewer: React.FC<InteractiveSVGViewerProps> = ({ svgContent, title = "Azure Architecture Diagram" }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  useEffect(() => {
    if (!svgContent || !containerRef.current) return;

    // Clear previous content
    containerRef.current.innerHTML = "";

    // Create a wrapper div for the SVG
    const wrapper = document.createElement('div');
    wrapper.style.width = '100%';
    wrapper.style.height = '100%';
    wrapper.style.overflow = 'hidden';
    wrapper.style.position = 'relative';
    wrapper.style.cursor = 'grab';

    // Parse and insert SVG
    try {
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(svgContent, 'image/svg+xml');
      const svgElement = svgDoc.documentElement as unknown as SVGSVGElement;
      
      if (svgElement && svgElement.tagName === 'svg') {
        // Make SVG responsive and interactive
        svgElement.style.width = '100%';
        svgElement.style.height = 'auto';
        svgElement.style.maxWidth = 'none';
        svgElement.style.transition = 'transform 0.1s ease';
        svgElement.style.transformOrigin = 'center center';
        
        // Add interactive features
        svgElement.style.cursor = 'grab';
        
        // Store reference
        svgRef.current = svgElement;
        
        // Add event listeners for interactivity
        svgElement.addEventListener('mousedown', handleMouseDown);
        svgElement.addEventListener('mousemove', handleMouseMove);
        svgElement.addEventListener('mouseup', handleMouseUp);
        svgElement.addEventListener('mouseleave', handleMouseUp);
        svgElement.addEventListener('wheel', handleWheel, { passive: false });
        
        // Add click events to SVG elements for interactivity
        const clickableElements = svgElement.querySelectorAll('g, rect, ellipse, polygon, text');
        clickableElements.forEach((element) => {
          element.addEventListener('click', (e) => {
            e.stopPropagation();
            // Add click feedback
            const originalFill = (element as SVGElement).style.fill;
            (element as SVGElement).style.fill = '#007acc';
            setTimeout(() => {
              (element as SVGElement).style.fill = originalFill;
            }, 200);
          });
          
          // Add hover effects
          element.addEventListener('mouseenter', () => {
            (element as SVGElement).style.filter = 'brightness(1.1)';
            (element as SVGElement).style.cursor = 'pointer';
          });
          
          element.addEventListener('mouseleave', () => {
            (element as SVGElement).style.filter = 'none';
          });
        });
        
        wrapper.appendChild(svgElement);
        containerRef.current.appendChild(wrapper);
        
        // Initial fit to container
        fitToContainer();
      } else {
        throw new Error('Invalid SVG content');
      }
    } catch (error) {
      console.error('Error parsing SVG:', error);
      containerRef.current.innerHTML = '<p style="color: red; text-align: center; padding: 20px;">Error loading interactive diagram</p>';
    }

    return () => {
      if (svgRef.current) {
        svgRef.current.removeEventListener('mousedown', handleMouseDown);
        svgRef.current.removeEventListener('mousemove', handleMouseMove);
        svgRef.current.removeEventListener('mouseup', handleMouseUp);
        svgRef.current.removeEventListener('mouseleave', handleMouseUp);
        svgRef.current.removeEventListener('wheel', handleWheel);
      }
    };
  }, [svgContent]);

  const handleMouseDown = (e: MouseEvent) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - position.x, y: e.clientY - position.y });
    if (svgRef.current) {
      svgRef.current.style.cursor = 'grabbing';
    }
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (!isDragging) return;
    
    const newPosition = {
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    };
    setPosition(newPosition);
    updateTransform(scale, newPosition);
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    if (svgRef.current) {
      svgRef.current.style.cursor = 'grab';
    }
  };

  const handleWheel = (e: WheelEvent) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    const newScale = Math.max(0.1, Math.min(3, scale * delta));
    setScale(newScale);
    updateTransform(newScale, position);
  };

  const updateTransform = (newScale: number, newPosition: { x: number; y: number }) => {
    if (svgRef.current) {
      svgRef.current.style.transform = `scale(${newScale}) translate(${newPosition.x / newScale}px, ${newPosition.y / newScale}px)`;
    }
  };

  const zoomIn = () => {
    const newScale = Math.min(3, scale * 1.2);
    setScale(newScale);
    updateTransform(newScale, position);
  };

  const zoomOut = () => {
    const newScale = Math.max(0.1, scale * 0.8);
    setScale(newScale);
    updateTransform(newScale, position);
  };

  const resetView = () => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
    updateTransform(1, { x: 0, y: 0 });
  };

  const fitToContainer = () => {
    if (!containerRef.current || !svgRef.current) return;
    
    const containerRect = containerRef.current.getBoundingClientRect();
    const svgRect = svgRef.current.getBoundingClientRect();
    
    const scaleX = containerRect.width / svgRect.width;
    const scaleY = containerRect.height / svgRect.height;
    const newScale = Math.min(scaleX, scaleY, 1) * 0.9;
    
    setScale(newScale);
    setPosition({ x: 0, y: 0 });
    updateTransform(newScale, { x: 0, y: 0 });
  };

  if (!svgContent) {
    return (
      <Box textAlign="center" p="8" color="gray.500">
        <Text>No interactive diagram available</Text>
      </Box>
    );
  }

  return (
    <VStack spacing="4" align="stretch" h="100%">
      <HStack justify="space-between" align="center">
        <Text fontSize="sm" color="blue.600" fontWeight="medium">
          🎯 {title} (Interactive)
        </Text>
        <HStack spacing="2">
          <Tooltip label="Zoom In">
            <IconButton
              aria-label="Zoom In"
              icon={<span>🔍+</span>}
              size="sm"
              onClick={zoomIn}
              isDisabled={scale >= 3}
            />
          </Tooltip>
          <Tooltip label="Zoom Out">
            <IconButton
              aria-label="Zoom Out"
              icon={<span>🔍-</span>}
              size="sm"
              onClick={zoomOut}
              isDisabled={scale <= 0.1}
            />
          </Tooltip>
          <Tooltip label="Reset View">
            <IconButton
              aria-label="Reset View"
              icon={<span>🎯</span>}
              size="sm"
              onClick={resetView}
            />
          </Tooltip>
          <Tooltip label="Fit to Container">
            <IconButton
              aria-label="Fit to Container"
              icon={<span>📐</span>}
              size="sm"
              onClick={fitToContainer}
            />
          </Tooltip>
        </HStack>
      </HStack>
      
      <Box
        ref={containerRef}
        border="1px solid"
        borderColor="gray.200"
        borderRadius="md"
        bg="white"
        h="500px"
        overflow="hidden"
        position="relative"
        userSelect="none"
      />
      
      <Text fontSize="xs" color="gray.500" textAlign="center">
        🖱️ Click and drag to pan • 🎯 Scroll to zoom • 📐 Click elements for interaction
      </Text>
    </VStack>
  );
};

export default InteractiveSVGViewer;