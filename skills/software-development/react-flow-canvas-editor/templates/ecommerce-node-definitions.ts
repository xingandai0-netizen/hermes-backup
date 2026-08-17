// E-commerce AI Workflow Node Definitions
// Copy and modify for your project

import type { NodeCategory, PortDefinition } from '@/types/workflow';

interface NodeDefinition {
  type: string;
  label: string;
  category: NodeCategory;
  flowType: string;
  description: string;
  inputs: PortDefinition[];
  outputs: PortDefinition[];
  defaultConfig: Record<string, unknown>;
}

export const NODE_DEFINITIONS: NodeDefinition[] = [
  // === INPUT NODES ===
  {
    type: 'skuImport',
    label: 'SKU批量导入',
    category: 'INPUT',
    flowType: 'skuImport',
    description: '从CSV/Excel导入SKU数据',
    inputs: [],
    outputs: [{ id: 'data', name: 'data', type: 'DATA', label: 'SKU数据' }],
    defaultConfig: { fileName: '', columnMapping: {}, rowCount: 0 },
  },

  // === AI GENERATION NODES ===
  {
    type: 'imageGen',
    label: '图片生成',
    category: 'AI_GENERATION',
    flowType: 'imageGen',
    description: 'GPT-Image-2 AI图片生成',
    inputs: [{ id: 'prompt', name: 'prompt', type: 'TEXT', label: 'Prompt' }],
    outputs: [{ id: 'image', name: 'image', type: 'IMAGE', label: '生成图片' }],
    defaultConfig: { prompt: '', n: 1, size: '1024x1024', quality: 'standard' },
  },
  {
    type: 'videoGen',
    label: '视频生成',
    category: 'AI_GENERATION',
    flowType: 'videoGen',
    description: 'Seedance 2 AI视频生成',
    inputs: [{ id: 'prompt', name: 'prompt', type: 'TEXT', label: 'Prompt' }],
    outputs: [{ id: 'video', name: 'video', type: 'VIDEO', label: '生成视频' }],
    defaultConfig: { prompt: '', duration: 5, resolution: '720p' },
  },

  // === PROCESSING NODES ===
  {
    type: 'imageProcess',
    label: '图片处理',
    category: 'PROCESSING',
    flowType: 'imageProcess',
    description: '抠图/裁剪/调色/水印',
    inputs: [{ id: 'image', name: 'image', type: 'IMAGE', label: '输入图片' }],
    outputs: [{ id: 'image', name: 'image', type: 'IMAGE', label: '处理结果' }],
    defaultConfig: { operation: '抠图', quality: 95 },
  },
  {
    type: 'sizeAdapter',
    label: '尺寸适配',
    category: 'PROCESSING',
    flowType: 'sizeAdapter',
    description: '适配电商平台图片尺寸',
    inputs: [{ id: 'image', name: 'image', type: 'IMAGE', label: '输入图片' }],
    outputs: [{ id: 'image', name: 'image', type: 'IMAGE', label: '适配结果' }],
    defaultConfig: { width: 800, height: 800, preset: 'taobao_main', mode: 'contain' },
  },

  // === OUTPUT NODES ===
  {
    type: 'export',
    label: '导出',
    category: 'OUTPUT',
    flowType: 'export',
    description: '下载或推送到平台',
    inputs: [
      { id: 'image', name: 'image', type: 'IMAGE', label: '图片' },
      { id: 'video', name: 'video', type: 'VIDEO', label: '视频' },
    ],
    outputs: [],
    defaultConfig: { format: 'png', quality: 95, destination: 'download' },
  },
];

// E-commerce size presets
export const IMAGE_SIZE_PRESETS = {
  taobao_main: { label: '淘宝主图', width: 800, height: 800 },
  taobao_detail: { label: '淘宝详情', width: 750, height: 1000 },
  douyin_vertical: { label: '抖音竖版', width: 1080, height: 1920 },
  xiaohongshu: { label: '小红书', width: 1080, height: 1440 },
  wechat_moments: { label: '朋友圈广告', width: 1080, height: 1080 },
  pdd_main: { label: '拼多多主图', width: 750, height: 750 },
  jd_main: { label: '京东主图', width: 800, height: 800 },
  horizontal_video: { label: '横版视频', width: 1920, height: 1080 },
};

// Port colors by type
export const PORT_COLORS: Record<string, string> = {
  IMAGE: '#3b82f6',   // blue
  VIDEO: '#a855f7',   // purple
  TEXT: '#22c55e',    // green
  DATA: '#f97316',    // orange
};

// Node category labels and colors
export const NODE_CATEGORY_LABELS: Record<string, string> = {
  INPUT: '输入',
  AI_GENERATION: 'AI生成',
  PROCESSING: '处理',
  OUTPUT: '输出',
};

export const NODE_CATEGORY_COLORS: Record<string, string> = {
  INPUT: '#22c55e',
  AI_GENERATION: '#a855f7',
  PROCESSING: '#3b82f6',
  OUTPUT: '#f97316',
};
