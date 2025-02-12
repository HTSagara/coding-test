<template>
  <v-container>
    <v-row>
      <v-col>
        <v-btn color="primary" @click="openUserDialog()" class="mb-4"> Create User </v-btn>

        <v-data-table :headers="headers" :items="users" :loading="loading" class="elevation-1">
          <template v-slot:item.username="{ item }">
            <router-link :to="'/user/' + item._id">
              {{ item.username }}
            </router-link>
          </template>

          <template v-slot:item.roles="{ item }">
            <v-chip v-for="role in item.roles" :key="role" class="mr-1" small>
              {{ role }}
            </v-chip>
          </template>

          <template v-slot:item.active="{ item }">
            <v-chip :color="item.active ? 'green' : 'red'" small>
              {{ item.active ? 'Active' : 'Inactive' }}
            </v-chip>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="openUserDialog(item)"> mdi-pencil </v-icon>
            <v-icon small @click="confirmDelete(item)"> mdi-delete </v-icon>
          </template>
        </v-data-table>

        <!-- User Dialog -->
        <user-dialog v-model="dialog" :user="selectedUser" @save="saveUser" />

        <!-- Delete Confirmation -->
        <v-dialog v-model="deleteDialog" max-width="400">
          <v-card>
            <v-card-title>Confirm Delete</v-card-title>
            <v-card-text> Are you sure you want to delete this user? </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="grey darken-1" text @click="deleteDialog = false"> Cancel </v-btn>
              <v-btn color="red darken-1" text @click="deleteUser"> Delete </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import UserDialog from './UserDialog.vue'
import axios from 'axios'

export default {
  name: 'UserTable',

  components: {
    UserDialog,
  },

  data: () => ({
    headers: [
      { text: 'Username', value: 'username' },
      { text: 'Roles', value: 'roles' },
      { text: 'Timezone', value: 'preferences.timezone' },
      { text: 'Active', value: 'active' },
      { text: 'Created At', value: 'created_ts' },
      { text: 'Actions', value: 'actions', sortable: false },
    ],
    users: [],
    loading: false,
    dialog: false,
    deleteDialog: false,
    selectedUser: null,
  }),

  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:8080/api/users')
        this.users = response.data
      } catch (error) {
        console.error('Error fetching users:', error)
      }
      this.loading = false
    },

    openUserDialog(user = null) {
      this.selectedUser = user
      this.dialog = true
    },

    async saveUser(userData) {
      try {
        if (userData._id) {
          await axios.put(`http://localhost:5000/api/users/${userData._id}`, userData)
        } else {
          await axios.post('http://localhost:5000/api/users', userData)
        }
        this.fetchUsers()
        this.dialog = false
      } catch (error) {
        console.error('Error saving user:', error)
      }
    },

    confirmDelete(user) {
      this.selectedUser = user
      this.deleteDialog = true
    },

    async deleteUser() {
      try {
        await axios.delete(`http://localhost:5000/api/users/${this.selectedUser._id}`)
        this.fetchUsers()
        this.deleteDialog = false
      } catch (error) {
        console.error('Error deleting user:', error)
      }
    },
  },

  mounted() {
    this.fetchUsers()
  },
}
</script>
