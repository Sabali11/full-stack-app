import React from "react";

const ContactList = ({ contacts, onUpdate, onDelete, editingId, editForm, handleEditChange, handleEditSubmit, handleCancel }) => {
  return (
    <div>
      <h2>Contacts</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>FirstName</th>
            <th>LastName</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map(contact => (
            <tr key={contact.id}>
              {editingId === contact.id ? (
                <>
                  <td>
                    <input
                      name="firstName"
                      value={editForm.firstName}
                      onChange={handleEditChange}
                    />
                  </td>
                  <td>
                    <input
                      name="lastName"
                      value={editForm.lastName}
                      onChange={handleEditChange}
                    />
                  </td>
                  <td>
                    <input
                      name="email"
                      value={editForm.email}
                      onChange={handleEditChange}
                    />
                  </td>
                  <td>
                    <button onClick={() => handleEditSubmit(contact.id)}>Save</button>
                    <button onClick={handleCancel}>Cancel</button>
                  </td>
                </>
              ) : (
                <>
                  <td>{contact.firstName}</td>
                  <td>{contact.lastName}</td>
                  <td>{contact.email}</td>
                  <td>
                    <button onClick={() => onUpdate(contact)}>Update</button>
                    <button onClick={() => onDelete(contact.id)}>Delete</button>
                  </td>
                </>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ContactList;
