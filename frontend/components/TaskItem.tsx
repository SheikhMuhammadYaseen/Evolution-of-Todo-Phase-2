'use client'

import { Task } from '@/lib/types'
import { useState } from 'react'

interface TaskItemProps {
  task: Task
  onToggle: (id: number) => Promise<void>
  onUpdate: (id: number, title: string, description?: string) => Promise<void>
  onDelete: (id: number) => Promise<void>
}

export default function TaskItem({ task, onToggle, onUpdate, onDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(task.title)
  const [editDescription, setEditDescription] = useState(task.description || '')

  const handleSave = async () => {
    if (editTitle.trim()) {
      await onUpdate(task.id, editTitle, editDescription)
      setIsEditing(false)
    }
  }

  const handleCancel = () => {
    setEditTitle(task.title)
    setEditDescription(task.description || '')
    setIsEditing(false)
  }

  if (isEditing) {
    return (
      <div className="rounded-lg border bg-white p-4 shadow-sm">
        <input
          type="text"
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          maxLength={500}
          className="mb-2 w-full rounded-md border px-3 py-2"
          placeholder="Task title"
        />
        <textarea
          value={editDescription}
          onChange={(e) => setEditDescription(e.target.value)}
          maxLength={10000}
          rows={3}
          className="mb-3 w-full rounded-md border px-3 py-2"
          placeholder="Task description (optional)"
        />
        <div className="flex gap-2">
          <button
            onClick={handleSave}
            className="rounded-md bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
          >
            Save
          </button>
          <button
            onClick={handleCancel}
            className="rounded-md bg-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-400"
          >
            Cancel
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex items-start gap-3 rounded-lg border bg-white p-4 shadow-sm">
      <input
        type="checkbox"
        checked={task.status}
        onChange={() => onToggle(task.id)}
        className="mt-1 h-5 w-5 rounded"
      />

      <div className="flex-1">
        <h3
          className={`font-medium ${
            task.status ? 'text-gray-500 line-through' : 'text-gray-900'
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p className="mt-1 text-sm text-gray-600">{task.description}</p>
        )}
        <p className="mt-2 text-xs text-gray-400">
          Created: {new Date(task.created_at).toLocaleDateString()}
        </p>
      </div>

      <div className="flex gap-2">
        <button
          onClick={() => setIsEditing(true)}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="text-sm text-red-600 hover:text-red-800"
        >
          Delete
        </button>
      </div>
    </div>
  )
}
