---
title: "Git Git Submodules vs. Git Subtree"
date: 2024-05-26T19:45:11+0000
lastmod: 2024-05-26T19:45:11+0000
slug: "integrating-external-git-repositories-git-submodules-vs-git-subtree"
summary: "Integrate external Git repositories using Git submodules or subtree. This guide covers the steps for both methods and compares their features. Simplify your development workflow and maintain modular codebases by choosing the best approach for your needs, enhancing code reusability and efficiency."
tags: ["csharp", "git", "code"]
feature_image: "/images/2024/05/1-AureuyXYDYHHU-jUMv_00A.webp"
aliases:
  - /integrating-external-git-repositories-git-submodules-vs-git-subtree/
---

### Integrating External Git Repositories: Git Submodules vs. Git Subtree

We all desire in software development for reusability and modularity, which are key to maintaining efficient and scalable codebases. I'm often needing to reuse a project from a different GitHub repository within the same organization. Two popular methods for this are Git submodules and Git subtree. Below I'll show you two paths on how to integrate an external repository into your C# project using both Git submodules and Git subtree with Visual Studio Code (VSCode), and provide a comparison to help you choose the best approach for your needs.

### Using Git Submodules

Git submodules allow you to keep a Git repository as a subdirectory of another Git repository. This can be useful for sharing code across multiple projects.

#### Step 1: Clone Your Main Repository

First, clone your main repository where you want to include the submodule.

```bash
git clone https://github.com/your-org/main-repo.git
cd main-repo

```

#### Step 2: Add the Submodule

Add the submodule to your main repository.

```bash
git submodule add https://github.com/your-org/reusable-project.git path/to/submodule

```

Replace `path/to/submodule` with the path where you want to add the submodule within your main repository.

#### Step 3: Initialize and Update the Submodule

Initialize and update the submodule to clone the code.

```bash
git submodule init
git submodule update

```

#### Step 4: Configure Your Project to Use the Submodule

In your main project, reference the project files from the submodule.

1. **Open VSCode**: Open your main project in VSCode.
2. **Add Existing Project**: Add the existing project from the submodule to your solution.

- Open the `.sln` file in VSCode or use the terminal:

```bash
dotnet sln add path/to/submodule/project.csproj

```

1. **Reference the Project**: Add a project reference to the submodule project:

```xml
<ItemGroup>
  <ProjectReference Include="path/to/submodule/project.csproj" />
</ItemGroup>

```

#### Step 5: Commit and Push Changes

Commit and push the changes to your repository to include the submodule configuration.

```bash
git add .
git commit -m "Added submodule for reusable project"
git push origin main

```

#### Cloning the Repository with Submodules

When someone else clones your repository, they need to initialize and update the submodules as well.

```bash
git clone --recurse-submodules https://github.com/your-org/main-repo.git

```

Or, if they have already cloned the repository:

```bash
git submodule init
git submodule update

```

### Using Git Subtree

Git subtree allows you to merge a repository into a subdirectory of another repository and keep it updated without the complexity of submodules.

#### Step 1: Add the Subtree

First, add the repository as a subtree.

```bash
git remote add reusable-project https://github.com/your-org/reusable-project.git
git subtree add --prefix=path/to/submodule reusable-project main --squash

```

- `--prefix=path/to/submodule`: Specifies the directory where you want the subtree to appear.
- `main`: The branch of the reusable project you want to add.
- `--squash`: Combines the commit history of the subtree into a single commit.

#### Step 2: Fetch Updates from the Subtree

To update the subtree with the latest changes from the upstream repository, you can pull updates.

```bash
git subtree pull --prefix=path/to/submodule reusable-project main --squash

```

#### Step 3: Push Changes Back to the Subtree

If you make changes to the subtree and want to push them back to the upstream repository, use:

```bash
git subtree push --prefix=path/to/submodule reusable-project main

```

#### Step 4: Configure Your Project to Use the Subtree

Configure your main project to reference the subtree project.

1. **Open VSCode**: Open your main project in VSCode.
2. **Add Existing Project**: Add the existing project from the subtree to your solution.

- Open the `.sln` file in VSCode or use the terminal:

```bash
dotnet sln add path/to/submodule/project.csproj

```

1. **Reference the Project**: Add a project reference to the subtree project:

```xml
<ItemGroup>
  <ProjectReference Include="path/to/submodule/project.csproj" />
</ItemGroup>

```

### Example Repository Structure

#### With Submodules

```
main-repo/
├── .git
├── .gitmodules
├── MainProject/
│   └── MainProject.csproj
├── reusable-project/ (submodule)
│   └── ReusableProject.csproj
└── MainSolution.sln

```

#### With Subtree

```
main-repo/
├── .git
├── MainProject/
│   └── MainProject.csproj
├── path/to/submodule/ (subtree)
│   └── ReusableProject.csproj
└── MainSolution.sln

```

### Comparison Table

| Feature | Git Submodules | Git Subtree |
| --- | --- | --- |
| Workflow | Requires separate commands for init and update | Integrated into main repository |
| Repository Management | Multiple repositories | Single repository |
| Commit History | Preserves original commit history | Can squash commits into a single commit |
| Detached HEAD Issues | Possible | Not applicable |
| Complexity | More complex | Simpler |
| Contributing Back Changes | More steps involved | Direct push to upstream |

### Conclusion

Both Git submodules and Git subtree provide effective ways to integrate external repositories into your main project. Submodules offer a way to keep commit histories separate and maintain clear boundaries between projects, but they come with additional complexity and management overhead. Subtree, on the other hand, provides a more seamless integration, simplifying the process of updating and managing external code.

By leveraging the right tool for your needs, you can enhance your development workflow and promote code reusability. Whether you choose submodules or subtree, both methods will help you maintain modular and reusable codebases, leading to more efficient and scalable projects.

Happy coding!
