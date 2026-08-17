#!/usr/bin/env python3
"""
Hermes记忆系统 - 基于MemOS的学习成果
为Hermes Agent提供持久化、可检索、可编辑的记忆功能
"""

import json
import sqlite3
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HermesMemory:
    """Hermes记忆系统 - 统一记忆API"""
    
    def __init__(self, memory_dir: str = "~/.hermes/memory"):
        self.memory_dir = Path(memory_dir).expanduser()
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self.db_path = self.memory_dir / "memories.db"
        self._init_database()
        
        # 记忆缓存
        self.cache = {}
        self.cache_size = 1000
    
    def _init_database(self):
        """初始化记忆数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建记忆表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                category TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                last_accessed TIMESTAMP,
                tags TEXT,
                embedding_vector BLOB
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_key ON memories(key)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON memories(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at)')
        
        # 创建全文搜索虚拟表
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts 
            USING fts5(key, value, category, tags, content='memories', content_rowid='rowid')
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"记忆数据库初始化完成: {self.db_path}")
    
    def save(self, key: str, value: Any, category: str = "general", 
             tags: List[str] = None, metadata: Dict[str, Any] = None) -> str:
        """
        保存记忆
        
        Args:
            key: 记忆键
            value: 记忆值
            category: 记忆类别
            tags: 标签列表
            metadata: 元数据
            
        Returns:
            记忆ID
        """
        # 生成记忆ID
        memory_id = self._generate_memory_id(key, category)
        
        # 序列化值
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value, ensure_ascii=False)
        else:
            value_str = str(value)
        
        # 处理标签
        tags_str = json.dumps(tags or [])
        
        # 处理元数据
        metadata_str = json.dumps(metadata or {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 插入或替换记忆
            cursor.execute('''
                INSERT OR REPLACE INTO memories 
                (id, key, value, category, tags, metadata, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (memory_id, key, value_str, category, tags_str, metadata_str, 
                  datetime.now().isoformat()))
            
            # 更新FTS索引
            cursor.execute('''
                INSERT OR REPLACE INTO memories_fts 
                (rowid, key, value, category, tags)
                VALUES (
                    (SELECT rowid FROM memories WHERE id = ?),
                    ?, ?, ?, ?
                )
            ''', (memory_id, key, value_str, category, tags_str))
            
            conn.commit()
            
            # 更新缓存
            self.cache[memory_id] = {
                'key': key,
                'value': value,
                'category': category,
                'tags': tags or [],
                'metadata': metadata or {}
            }
            
            logger.info(f"记忆已保存: {key} (类别: {category})")
            return memory_id
            
        except Exception as e:
            logger.error(f"保存记忆失败: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get(self, key: str, category: Optional[str] = None) -> Optional[Any]:
        """
        获取记忆
        
        Args:
            key: 记忆键
            category: 记忆类别（可选）
            
        Returns:
            记忆值，如果不存在则返回None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if category:
                cursor.execute('''
                    SELECT value, id FROM memories 
                    WHERE key = ? AND category = ?
                    ORDER BY updated_at DESC LIMIT 1
                ''', (key, category))
            else:
                cursor.execute('''
                    SELECT value, id FROM memories 
                    WHERE key = ?
                    ORDER BY updated_at DESC LIMIT 1
                ''', (key,))
            
            result = cursor.fetchone()
            
            if result:
                value_str, memory_id = result
                
                # 更新访问统计
                cursor.execute('''
                    UPDATE memories 
                    SET access_count = access_count + 1, 
                        last_accessed = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), memory_id))
                conn.commit()
                
                # 反序列化值
                try:
                    value = json.loads(value_str)
                except (json.JSONDecodeError, TypeError):
                    value = value_str
                
                # 更新缓存
                self.cache[memory_id] = value
                
                return value
            
            return None
            
        finally:
            conn.close()
    
    def search(self, query: str, category: Optional[str] = None, 
               limit: int = 10) -> List[Dict[str, Any]]:
        """
        搜索记忆
        
        Args:
            query: 搜索查询
            category: 记忆类别（可选）
            limit: 返回结果数量限制
            
        Returns:
            记忆列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 使用FTS5进行全文搜索
            if category:
                cursor.execute('''
                    SELECT m.key, m.value, m.category, m.tags, m.metadata,
                           m.created_at, m.updated_at, m.access_count
                    FROM memories m
                    JOIN memories_fts fts ON m.rowid = fts.rowid
                    WHERE memories_fts MATCH ? AND m.category = ?
                    ORDER BY rank
                    LIMIT ?
                ''', (query, category, limit))
            else:
                cursor.execute('''
                    SELECT m.key, m.value, m.category, m.tags, m.metadata,
                           m.created_at, m.updated_at, m.access_count
                    FROM memories m
                    JOIN memories_fts fts ON m.rowid = fts.rowid
                    WHERE memories_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                ''', (query, limit))
            
            results = []
            for row in cursor.fetchall():
                key, value_str, cat, tags_str, metadata_str, created_at, updated_at, access_count = row
                
                # 反序列化
                try:
                    value = json.loads(value_str)
                except (json.JSONDecodeError, TypeError):
                    value = value_str
                
                try:
                    tags = json.loads(tags_str)
                except (json.JSONDecodeError, TypeError):
                    tags = []
                
                try:
                    metadata = json.loads(metadata_str)
                except (json.JSONDecodeError, TypeError):
                    metadata = {}
                
                results.append({
                    'key': key,
                    'value': value,
                    'category': cat,
                    'tags': tags,
                    'metadata': metadata,
                    'created_at': created_at,
                    'updated_at': updated_at,
                    'access_count': access_count
                })
            
            return results
            
        finally:
            conn.close()
    
    def update(self, key: str, value: Any, category: Optional[str] = None) -> bool:
        """
        更新记忆
        
        Args:
            key: 记忆键
            value: 新的记忆值
            category: 记忆类别（可选）
            
        Returns:
            是否更新成功
        """
        # 先检查记忆是否存在
        existing = self.get(key, category)
        
        if existing is not None:
            # 更新现有记忆
            memory_id = self._generate_memory_id(key, category or "general")
            
            # 序列化值
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, ensure_ascii=False)
            else:
                value_str = str(value)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    UPDATE memories 
                    SET value = ?, updated_at = ?
                    WHERE key = ? AND (? IS NULL OR category = ?)
                ''', (value_str, datetime.now().isoformat(), key, category, category))
                
                conn.commit()
                logger.info(f"记忆已更新: {key}")
                return True
                
            except Exception as e:
                logger.error(f"更新记忆失败: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()
        
        return False
    
    def delete(self, key: str, category: Optional[str] = None) -> bool:
        """
        删除记忆
        
        Args:
            key: 记忆键
            category: 记忆类别（可选）
            
        Returns:
            是否删除成功
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if category:
                cursor.execute('DELETE FROM memories WHERE key = ? AND category = ?', (key, category))
            else:
                cursor.execute('DELETE FROM memories WHERE key = ?', (key,))
            
            conn.commit()
            
            # 从缓存中移除
            keys_to_remove = [k for k, v in self.cache.items() if v.get('key') == key]
            for k in keys_to_remove:
                del self.cache[k]
            
            logger.info(f"记忆已删除: {key}")
            return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"删除记忆失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def list_categories(self) -> List[str]:
        """列出所有记忆类别"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT DISTINCT category FROM memories ORDER BY category')
            categories = [row[0] for row in cursor.fetchall()]
            return categories
        finally:
            conn.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 总记忆数
            cursor.execute('SELECT COUNT(*) FROM memories')
            total_count = cursor.fetchone()[0]
            
            # 按类别统计
            cursor.execute('''
                SELECT category, COUNT(*) 
                FROM memories 
                GROUP BY category 
                ORDER BY COUNT(*) DESC
            ''')
            category_stats = dict(cursor.fetchall())
            
            # 总访问次数
            cursor.execute('SELECT SUM(access_count) FROM memories')
            total_access = cursor.fetchone()[0] or 0
            
            # 最近更新的记忆
            cursor.execute('''
                SELECT key, category, updated_at 
                FROM memories 
                ORDER BY updated_at DESC 
                LIMIT 5
            ''')
            recent_memories = [
                {'key': key, 'category': cat, 'updated_at': updated_at}
                for key, cat, updated_at in cursor.fetchall()
            ]
            
            return {
                'total_count': total_count,
                'category_stats': category_stats,
                'total_access': total_access,
                'recent_memories': recent_memories,
                'cache_size': len(self.cache),
                'database_size': self.db_path.stat().st_size if self.db_path.exists() else 0
            }
        finally:
            conn.close()
    
    def backup(self, backup_path: Optional[str] = None) -> str:
        """备份记忆数据库"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = str(self.memory_dir / f"backup_{timestamp}.db")
        
        backup_file = Path(backup_path)
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制数据库文件
        import shutil
        shutil.copy2(self.db_path, backup_file)
        
        logger.info(f"记忆备份完成: {backup_file}")
        return str(backup_file)
    
    def restore(self, backup_path: str) -> bool:
        """恢复记忆数据库"""
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            logger.error(f"备份文件不存在: {backup_path}")
            return False
        
        try:
            import shutil
            shutil.copy2(backup_file, self.db_path)
            
            # 清空缓存
            self.cache.clear()
            
            logger.info(f"记忆恢复完成: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"记忆恢复失败: {e}")
            return False
    
    def _generate_memory_id(self, key: str, category: str) -> str:
        """生成记忆ID"""
        content = f"{key}:{category}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
        logger.info("记忆缓存已清空")
    
    def optimize(self):
        """优化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 重建FTS索引
            cursor.execute('INSERT INTO memories_fts(memories_fts) VALUES("rebuild")')
            
            # 清理过期的缓存
            self.cache.clear()
            
            conn.commit()
            logger.info("记忆数据库优化完成")
        except Exception as e:
            logger.error(f"数据库优化失败: {e}")
            conn.rollback()
        finally:
            conn.close()


class HermesMemoryManager:
    """Hermes记忆管理器 - 提供高级记忆管理功能"""
    
    def __init__(self, memory_dir: str = "~/.hermes/memory"):
        self.memory = HermesMemory(memory_dir)
        
        # 预定义的记忆类别
        self.categories = {
            'user_preferences': '用户偏好',
            'environment_facts': '环境事实',
            'skill_knowledge': '技能知识',
            'project_context': '项目上下文',
            'conversation_history': '对话历史',
            'learned_patterns': '学习模式',
            'error_patterns': '错误模式',
            'performance_metrics': '性能指标'
        }
    
    def save_user_preference(self, key: str, value: Any, 
                            description: Optional[str] = None) -> str:
        """保存用户偏好"""
        metadata = {}
        if description:
            metadata['description'] = description
        
        return self.memory.save(
            key=key,
            value=value,
            category='user_preferences',
            tags=['preference', 'user'],
            metadata=metadata
        )
    
    def save_environment_fact(self, key: str, value: Any, 
                             source: Optional[str] = None) -> str:
        """保存环境事实"""
        metadata = {}
        if source:
            metadata['source'] = source
        
        return self.memory.save(
            key=key,
            value=value,
            category='environment_facts',
            tags=['environment', 'fact'],
            metadata=metadata
        )
    
    def save_skill_knowledge(self, skill_name: str, knowledge: Dict[str, Any], 
                            version: Optional[str] = None) -> str:
        """保存技能知识"""
        metadata = {
            'skill_name': skill_name,
            'version': version or '1.0.0'
        }
        
        return self.memory.save(
            key=f"skill_{skill_name}",
            value=knowledge,
            category='skill_knowledge',
            tags=['skill', skill_name],
            metadata=metadata
        )
    
    def save_project_context(self, project_name: str, context: Dict[str, Any]) -> str:
        """保存项目上下文"""
        metadata = {
            'project_name': project_name,
            'last_updated': datetime.now().isoformat()
        }
        
        return self.memory.save(
            key=f"project_{project_name}",
            value=context,
            category='project_context',
            tags=['project', project_name],
            metadata=metadata
        )
    
    def save_conversation_insight(self, topic: str, insight: str, 
                                 importance: str = "medium") -> str:
        """保存对话洞察"""
        metadata = {
            'importance': importance,
            'timestamp': datetime.now().isoformat()
        }
        
        return self.memory.save(
            key=f"insight_{topic}",
            value=insight,
            category='conversation_history',
            tags=['insight', topic, importance],
            metadata=metadata
        )
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """获取所有用户偏好"""
        results = self.memory.search("*", category='user_preferences', limit=100)
        preferences = {}
        
        for result in results:
            preferences[result['key']] = result['value']
        
        return preferences
    
    def get_skill_knowledge(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """获取技能知识"""
        return self.memory.get(f"skill_{skill_name}", category='skill_knowledge')
    
    def get_project_context(self, project_name: str) -> Optional[Dict[str, Any]]:
        """获取项目上下文"""
        return self.memory.get(f"project_{project_name}", category='project_context')
    
    def search_insights(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """搜索对话洞察"""
        return self.memory.search(query, category='conversation_history', limit=limit)
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """获取记忆摘要"""
        stats = self.memory.get_stats()
        
        # 添加类别统计
        categories = self.memory.list_categories()
        category_info = {}
        
        for category in categories:
            category_memories = self.memory.search("*", category=category, limit=1)
            category_info[category] = {
                'count': len(category_memories),
                'description': self.categories.get(category, category)
            }
        
        return {
            'total_memories': stats['total_count'],
            'total_access': stats['total_access'],
            'categories': category_info,
            'recent_memories': stats['recent_memories']
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Hermes记忆系统')
    parser.add_argument('action', choices=['save', 'get', 'search', 'stats', 'backup', 'restore'])
    parser.add_argument('--key', '-k', help='记忆键')
    parser.add_argument('--value', '-v', help='记忆值')
    parser.add_argument('--category', '-c', help='记忆类别')
    parser.add_argument('--query', '-q', help='搜索查询')
    parser.add_argument('--file', '-f', help='文件路径')
    parser.add_argument('--backup-path', help='备份文件路径')
    
    args = parser.parse_args()
    
    memory = HermesMemory()
    
    if args.action == 'save':
        if not args.key or not args.value:
            print("错误: 需要提供 --key 和 --value")
            return
        
        # 尝试解析JSON值
        try:
            value = json.loads(args.value)
        except (json.JSONDecodeError, TypeError):
            value = args.value
        
        memory_id = memory.save(args.key, value, args.category or "general")
        print(f"记忆已保存: {memory_id}")
    
    elif args.action == 'get':
        if not args.key:
            print("错误: 需要提供 --key")
            return
        
        value = memory.get(args.key, args.category)
        if value is not None:
            print(json.dumps(value, ensure_ascii=False, indent=2))
        else:
            print("记忆未找到")
    
    elif args.action == 'search':
        if not args.query:
            print("错误: 需要提供 --query")
            return
        
        results = memory.search(args.query, args.category)
        print(f"找到 {len(results)} 个结果:")
        for result in results[:10]:
            print(f"  - {result['key']} ({result['category']}): {str(result['value'])[:50]}...")
    
    elif args.action == 'stats':
        stats = memory.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.action == 'backup':
        backup_path = memory.backup(args.backup_path)
        print(f"备份完成: {backup_path}")
    
    elif args.action == 'restore':
        if not args.backup_path:
            print("错误: 需要提供 --backup-path")
            return
        
        if memory.restore(args.backup_path):
            print("恢复完成")
        else:
            print("恢复失败")


if __name__ == '__main__':
    main()