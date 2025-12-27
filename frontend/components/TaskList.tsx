'use client'

import { Task } from '@/lib/types'
import TaskItem from './TaskItem'
import EmptyState from './EmptyState'

interface TaskListProps {
  tasks: Task[]
  onToggle: (id: number) => Promise<void>
  onUpdate: (id: number, title: string, description?: string) => Promise<void>
  onDelete: (id: number) => Promise<void>
}

export default function TaskList({ tasks, onToggle, onUpdate, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return <EmptyState />
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
