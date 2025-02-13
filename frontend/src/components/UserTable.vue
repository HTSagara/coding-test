// frontend/src/components/UserTable.vue
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-2xl font-bold mb-4">User List</h1>

        <!-- Create User Button -->
        <v-btn color="primary" dark class="mb-4" @click="openCreateModal">
          <v-icon left>mdi-plus</v-icon> Create User
        </v-btn>

        <!-- User Table -->
        <v-data-table
          :items="users"
          :headers="headers"
          item-value="_id"
          class="elevation-1"
          v-if="!loading && !error"
        >
          <template v-slot:item.username="{ item }">
            <router-link :to="`/users/${item._id}`" class="text-blue-600 underline">
              {{ item.username }}
            </router-link>
          </template>

          <template v-slot:item.roles="{ item }">
            {{ item.roles.join(', ') }}
          </template>

          <template v-slot:item.active="{ item }">
            <v-chip :color="item.active ? 'green' : 'red'" dark>
              {{ item.active ? 'Yes' : 'No' }}
            </v-chip>
          </template>

          <template v-slot:item.updated_ts="{ item }">
            {{ formatDate(item.updated_ts) }}
          </template>

          <template v-slot:item.created_ts="{ item }">
            {{ formatDate(item.created_ts) }}
          </template>

          <template v-slot:item.actions="{ item }">
            <v-btn icon color="yellow darken-2" @click="openEditModal(item)">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon color="red darken-2" @click="confirmDelete(item._id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>

        <v-alert v-if="loading" type="info">Loading...</v-alert>
        <v-alert v-if="error" type="error">{{ error }}</v-alert>
      </v-col>
    </v-row>

    <!-- Create/Edit User Dialog -->
    <v-dialog v-model="showModal" max-width="500px">
      <v-card>
        <v-card-title>{{ isEditing ? 'Edit User' : 'Create User' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="selectedUser.username" label="Username"></v-text-field>
          <v-text-field v-model="selectedUser.roles" label="Roles (comma-separated)"></v-text-field>
          <v-text-field v-model="selectedUser.preferences.timezone" label="Timezone"></v-text-field>
          <v-switch v-model="selectedUser.active" label="Active"></v-switch>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="showModal = false">Cancel</v-btn>
          <v-btn color="primary" @click="handleSave">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteConfirm" max-width="400px">
      <v-card>
        <v-card-title>Confirm Delete</v-card-title>
        <v-card-text>Are you sure you want to delete this user?</v-card-text>
        <v-card-actions>
          <v-btn text @click="showDeleteConfirm = false">Cancel</v-btn>
          <v-btn color="red darken-2" @click="deleteUser">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
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
  },
}
</script>
