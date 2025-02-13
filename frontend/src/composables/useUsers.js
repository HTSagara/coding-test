//frontend/src/composables/useUsers.js
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default function useUsers() {
  const users = ref([])
  const loading = ref(true)
  const error = ref(null)
  const showModal = ref(false)
  const showDeleteConfirm = ref(false)
  const selectedUser = ref({})
  const isEditing = ref(false)
  const userIdToDelete = ref(null)

  const headers = [
    { title: 'Username', key: 'username' },
    { title: 'Roles', key: 'roles' },
    { title: 'Timezone', key: 'preferences.timezone' },
    { title: 'Active', key: 'active' },
    { title: 'Last Updated At', key: 'updated_ts' },
    { title: 'Created At', key: 'created_ts' },
    { title: 'Actions', key: 'actions', sortable: false },
  ]

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/users')
      console.log('Fetched Users:', response.data) // Debugging output

      users.value = response.data.map((user) => ({
        ...user,
        roles: Array.isArray(user.roles) ? user.roles : [user.roles], // Ensure roles is an array
        preferences: user.preferences || { timezone: 'N/A' }, // Ensure preferences exist
      }))
    } catch (err) {
      error.value = 'Failed to fetch users'
      console.error('Error fetching users:', err)
    } finally {
      loading.value = false
    }
  }

  const openCreateModal = () => {
    selectedUser.value = { username: '', roles: [], preferences: { timezone: '' }, active: false }
    isEditing.value = false
    showModal.value = true
  }

  const openEditModal = (user) => {
    selectedUser.value = { ...user }
    isEditing.value = true
    showModal.value = true
  }

  const handleSave = async () => {
    try {
      if (isEditing.value) {
        await axios.put(
          `http://localhost:8000/api/users/${selectedUser.value._id}`,
          selectedUser.value,
        )
        const index = users.value.findIndex((u) => u._id === selectedUser.value._id)
        if (index !== -1) {
          users.value[index] = selectedUser.value
        }
      } else {
        const response = await axios.post('http://localhost:8000/api/users', selectedUser.value)
        users.value = [...users.value, response.data]
      }
      showModal.value = false
      await fetchUsers()
    } catch (err) {
      console.error('Error saving user:', err)
    }
  }

  const confirmDelete = (id) => {
    userIdToDelete.value = id
    showDeleteConfirm.value = true
  }

  const deleteUser = async () => {
    try {
      await axios.delete(`http://localhost:8000/api/users/${userIdToDelete.value}`)
      users.value = users.value.filter((user) => user._id !== userIdToDelete.value)
    } catch (err) {
      console.error('Error deleting user:', err)
    } finally {
      showDeleteConfirm.value = false
    }
  }

  const formatDate = (timestamp) => {
    return timestamp ? new Date(timestamp * 1000).toLocaleString() : 'N/A'
  }

  onMounted(fetchUsers)

  return {
    users,
    headers,
    loading,
    error,
    showModal,
    showDeleteConfirm,
    selectedUser,
    isEditing,
    openCreateModal,
    openEditModal,
    confirmDelete,
    deleteUser,
    handleSave,
    formatDate,
  }
}
