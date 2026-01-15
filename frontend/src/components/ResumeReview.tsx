import React, { useState, useMemo } from "react";
import type { BulletPatch } from "../api";

type Props = {
  patches: BulletPatch[];
  onPatchesChange: (patches: BulletPatch[]) => void;
};

export default function ResumeReview({ patches, onPatchesChange }: Props) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editText, setEditText] = useState("");

  // Group patches by project
  const groupedPatches = useMemo(() => {
    const groups: Record<string, BulletPatch[]> = {};
    patches.forEach((patch) => {
      const key = patch.project_key;
      if (!groups[key]) {
        groups[key] = [];
      }
      groups[key].push(patch);
    });
    return groups;
  }, [patches]);

  const handleAccept = (patchId: string) => {
    const updated = patches.map((p) =>
      p.id === patchId ? { ...p, accepted: true, edited_text: null } : p
    );
    onPatchesChange(updated);
    setEditingId(null);
  };

  const handleReject = (patchId: string) => {
    const updated = patches.map((p) =>
      p.id === patchId ? { ...p, accepted: false, edited_text: null } : p
    );
    onPatchesChange(updated);
    setEditingId(null);
  };

  const handleEdit = (patchId: string) => {
    const patch = patches.find((p) => p.id === patchId);
    if (patch) {
      setEditText(patch.edited_text || patch.rewritten);
      setEditingId(patchId);
    }
  };

  const handleSaveEdit = (patchId: string) => {
    const updated = patches.map((p) =>
      p.id === patchId
        ? { ...p, accepted: null, edited_text: editText }
        : p
    );
    onPatchesChange(updated);
    setEditingId(null);
    setEditText("");
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditText("");
  };

  const getDisplayText = (patch: BulletPatch): string => {
    if (patch.accepted === false) return patch.original;
    if (patch.edited_text) return patch.edited_text;
    if (patch.accepted === true) return patch.rewritten;
    return patch.rewritten; // default
  };

  const getStatus = (patch: BulletPatch): "accepted" | "rejected" | "edited" | "pending" => {
    if (patch.accepted === true) return "accepted";
    if (patch.accepted === false) return "rejected";
    if (patch.edited_text) return "edited";
    return "pending";
  };

  return (
    <div className="resumeReview">
      {Object.entries(groupedPatches).map(([projectKey, projectPatches]) => (
        <div key={projectKey} className="projectGroup">
          <h3 className="projectTitle">
            {projectPatches[0]?.project_title || projectKey}
          </h3>
          
          {projectPatches.map((patch) => (
            <div key={patch.id} className="bulletCard">
              <div className="bulletHeader">
                <span className={`statusBadge status-${getStatus(patch)}`}>
                  {getStatus(patch)}
                </span>
                <div className="bulletActions">
                  {editingId !== patch.id ? (
                    <>
                      <button
                        className="btnSmall btnAccept"
                        onClick={() => handleAccept(patch.id)}
                        disabled={patch.accepted === true}
                      >
                        ✓ Accept
                      </button>
                      <button
                        className="btnSmall btnReject"
                        onClick={() => handleReject(patch.id)}
                        disabled={patch.accepted === false}
                      >
                        ✗ Reject
                      </button>
                      <button
                        className="btnSmall btnEdit"
                        onClick={() => handleEdit(patch.id)}
                      >
                        ✎ Edit
                      </button>
                    </>
                  ) : (
                    <>
                      <button
                        className="btnSmall btnSave"
                        onClick={() => handleSaveEdit(patch.id)}
                      >
                        Save
                      </button>
                      <button
                        className="btnSmall btnCancel"
                        onClick={handleCancelEdit}
                      >
                        Cancel
                      </button>
                    </>
                  )}
                </div>
              </div>

              {editingId === patch.id ? (
                <textarea
                  className="editTextarea"
                  value={editText}
                  onChange={(e) => setEditText(e.target.value)}
                  rows={3}
                />
              ) : (
                <div className="bulletContent">
                  <div className="bulletText">{getDisplayText(patch)}</div>
                  {patch.accepted === false && (
                    <div className="originalLabel">Using original version</div>
                  )}
                  {patch.edited_text && (
                    <div className="editedLabel">Manually edited</div>
                  )}
                </div>
              )}

              {patch.accepted !== false && (
                <details className="comparison">
                  <summary className="comparisonToggle">Show original</summary>
                  <div className="originalText">{patch.original}</div>
                </details>
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

