import React, { useState, useEffect } from "react";
import ContactList from "./components/contactList";
import "./App.css";

function App() {
  const [contacts, setContacts] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({ firstName: "", lastName: "", email: "" });
  const [newContact, setNewContact] = useState({ firstName: "", lastName: "", email: "" });

  // Fetch contacts from API
  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    try {
      const response = await fetch("/contacts");
      const data = await response.json();
      setContacts(data.contacts);
    } catch (error) {
      console.error("Error fetching contacts:", error);
    }
  };

  // Create new contact
  const handleNewChange = (e) => {
    setNewContact({ ...newContact, [e.target.name]: e.target.value });
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await fetch("/contacts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newContact),
      });
      setNewContact({ firstName: "", lastName: "", email: "" });
      fetchContacts();
    } catch (error) {
      console.error(error);
    }
  };

  // Edit contact
  const handleEditClick = (contact) => {
    setEditingId(contact.id);
    setEditForm({
      firstName: contact.firstName,
      lastName: contact.lastName,
      email: contact.email,
    });
  };

  const handleEditChange = (e) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleEditSubmit = async (id) => {
    try {
      await fetch(`/contacts/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editForm),
      });
      setEditingId(null);
      fetchContacts();
    } catch (error) {
      console.error(error);
    }
  };

  // Delete contact
  const handleDelete = async (id) => {
    try {
      await fetch(`/contacts/${id}`, { method: "DELETE" });
      setContacts(contacts.filter(c => c.id !== id));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Contact Manager</h1>

      {/* Create Contact Form */}
      <form onSubmit={handleCreate} className="create-form">
        <input
          name="firstName"
          placeholder="First Name"
          value={newContact.firstName}
          onChange={handleNewChange}
          required
        />
        <input
          name="lastName"
          placeholder="Last Name"
          value={newContact.lastName}
          onChange={handleNewChange}
          required
        />
        <input
          name="email"
          placeholder="Email"
          value={newContact.email}
          onChange={handleNewChange}
          required
        />
        <button type="submit">Add Contact</button>
      </form>

      {/* Contacts Table */}
      <ContactList
        contacts={contacts}
        onUpdate={handleEditClick}
        onDelete={handleDelete}
        editingId={editingId}
        editForm={editForm}
        handleEditChange={handleEditChange}
        handleEditSubmit={handleEditSubmit}
        handleCancel={() => setEditingId(null)}
      />
    </div>
  );
}

export default App;
