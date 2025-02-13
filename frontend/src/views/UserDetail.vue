<template>
  <v-container>
    <v-btn color="primary" @click="$router.push('/')" class="mb-4">
      <v-icon left>mdi-arrow-left</v-icon>
      Back to User List
    </v-btn>

    <v-card class="mt-4">
      <v-card-title class="d-flex justify-space-between align-center">
        <span>User Details</span>
        <div>
          <v-btn icon color="yellow darken-2" class="mr-2" @click="openEditModal">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon color="red darken-2" @click="confirmDelete">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text v-if="!loading && !error">
        <v-list>
          <v-list-item>
            <v-list-item-title>Username</v-list-item-title>
            <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
          </v-list-item>

          <v-list-item>
            <v-list-item-title>Roles</v-list-item-title>
            <v-list-item-subtitle>{{ user.roles?.join(', ') }}</v-list-item-subtitle>
          </v-list-item>

          <v-list-item>
            <v-list-item-title>Timezone</v-list-item-title>
            <v-list-item-subtitle>{{ user.preferences?.timezone }}</v-list-item-subtitle>
          </v-list-item>

          <v-list-item>
            <v-list-item-title>Active</v-list-item-title>
            <v-list-item-subtitle>
              <v-chip :color="user.active ? 'green' : 'red'" dark>
                {{ user.active ? 'Yes' : 'No' }}
              </v-chip>
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item>
            <v-list-item-title>Last Updated At</v-list-item-title>
            <v-list-item-subtitle>{{ formatDate(user.updated_ts) }}</v-list-item-subtitle>
          </v-list-item>

          <v-list-item>
            <v-list-item-title>Created At</v-list-item-title>
            <v-list-item-subtitle>{{ formatDate(user.created_ts) }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-card-text>

      <v-alert v-if="loading" type="info">Loading...</v-alert>
      <v-alert v-if="error" type="error">{{ error }}</v-alert>
    </v-card>

    <!-- Edit User Dialog -->
    <v-dialog v-model="showEditModal" max-width="500px">
      <v-card>
        <v-card-title>Edit User</v-card-title>
        <v-card-text>
          <v-text-field v-model="editedUser.username" label="Username"></v-text-field>
          <v-text-field v-model="editedUser.roles" label="Roles (comma-separated)"></v-text-field>
          <v-text-field v-model="editedUser.preferences.timezone" label="Timezone"></v-text-field>
          <v-switch v-model="editedUser.active" label="Active"></v-switch>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="showEditModal = false">Cancel</v-btn>
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
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  props: ['id'],
  setup(props) {
    const router = useRouter()
    const user = ref({})
    const editedUser = ref({})
    const loading = ref(true)
    const error = ref(null)
    const showEditModal = ref(false)
    const showDeleteConfirm = ref(false)

    const fetchUser = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/users/${props.id}`)
        user.value = {
          ...response.data,
          roles: Array.isArray(response.data.roles) ? response.data.roles : [response.data.roles],
          preferences: response.data.preferences || { timezone: 'N/A' },
        }
      } catch (err) {
        error.value = 'Failed to fetch user details'
      } finally {
        loading.value = false
      }
    }

    const formatDate = (timestamp) => {
      return timestamp ? new Date(timestamp * 1000).toLocaleString() : 'N/A'
    }

    const openEditModal = () => {
      editedUser.value = { ...user.value }
      showEditModal.value = true
    }

    const handleSave = async () => {
      try {
        await axios.put(`http://localhost:8000/api/users/${props.id}`, editedUser.value)
        user.value = editedUser.value
        showEditModal.value = false
        await fetchUser()
      } catch (err) {
        error.value = 'Failed to update user'
        console.error('Error updating user:', err)
      }
    }

    const confirmDelete = () => {
      showDeleteConfirm.value = true
    }

    const deleteUser = async () => {
      try {
        await axios.delete(`http://localhost:8000/api/users/${props.id}`)
        router.push('/')
      } catch (err) {
        error.value = 'Failed to delete user'
        console.error('Error deleting user:', err)
      } finally {
        showDeleteConfirm.value = false
      }
    }

    onMounted(fetchUser)

    return {
      user,
      editedUser,
      loading,
      error,
      showEditModal,
      showDeleteConfirm,
      formatDate,
      openEditModal,
      handleSave,
      confirmDelete,
      deleteUser,
    }
  },
}
</script>
