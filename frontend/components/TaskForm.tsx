'use client'

import { useState } from 'react'
import { TaskCreate } from '@/lib/types'

interface TaskFormProps {
  onSubmit: (task: TaskCreate) => Promise<void>
  loading: boolean
}

export default function TaskForm({ onSubmit, loading }: TaskFormProps) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    await onSubmit({ title, description: description || undefined })

    // Reset form
    setTitle('')
    setDescription('')
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border bg-white p-6 shadow-sm">
      <h3 className="text-lg font-semibold">Add New Task</h3>

      <div>
        <label htmlFor="title" className="block text-sm font-medium">
          Title *
        </label>
        <input
          id="title"
          type="text"
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2"
          placeholder="What needs to be done?"
          maxLength={500}
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2"
          placeholder="Add more details (optional)"
          rows={3}
          maxLength={10000}
        />
      </div>

      <button
        type="submit"
        disabled={loading || !title.trim()}
        className="w-full rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  )
}
